from flask import Flask, request, render_template, send_file, abort
import os
import sys
import json
from carprice.util.util import read_yaml_file, write_yaml_file, get_carlist
from carprice.logger import logging
from carprice.config.configuration import ConfigurationManager
from carprice.constant import CONFIG_DIR, generate_timestamp
from carprice.pipeline.pipeline import TrainingPipeline
from carprice.entity.carprice_predictor import CarPricePredictor, CarPriceInputData
from carprice.logger import get_log_dataframe

# Constants for Directories and File Paths
ROOT_DIRECTORY = os.getcwd()
LOGS_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "carprice"
SAVED_MODELS_FOLDER_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIRECTORY, CONFIG_DIR, "model.yaml")
LOGS_DIR = os.path.join(ROOT_DIRECTORY, LOGS_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIRECTORY, PIPELINE_FOLDER_NAME)
SAVED_MODELS_DIR = os.path.join(ROOT_DIRECTORY, SAVED_MODELS_FOLDER_NAME)

# Keys for Context Data
CAR_DATA_KEY = "car_data"
PREDICTED_PRICE_KEY = "predicted_price"

# Initialize Flask App
app = Flask(__name__)


@app.route('/artifacts', defaults={'requested_path': 'carprice'})
@app.route('/artifacts/<path:requested_path>')
def render_artifacts_directory(requested_path):
    """
    Render the artifacts directory for browsing files.
    """
    os.makedirs("carprice", exist_ok=True)
    absolute_path = os.path.join(requested_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(absolute_path):
        return abort(404)

    # Serve file if it's a file
    if os.path.isfile(absolute_path):
        if ".html" in absolute_path:
            with open(absolute_path, "r", encoding="utf-8") as file:
                content = ''.join(file.readlines())
                return content
        return send_file(absolute_path)

    # Show directory contents
    files = {
        os.path.join(absolute_path, file_name): file_name
        for file_name in os.listdir(absolute_path)
        if "artifact" in os.path.join(absolute_path, file_name)
    }

    result = {
        "files": files,
        "parent_folder": os.path.dirname(absolute_path),
        "parent_label": absolute_path
    }
    return render_template('artifacts.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render the home page.
    """
    try:
        return render_template('home.html')
    except Exception as e:
        logging.exception(e)
        return str(e)


@app.route('/experiment-history', methods=['GET', 'POST'])
def view_experiment_history():
    """
    Display the history of experiments.
    """
    experiment_df = TrainingPipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    """
    Trigger the training pipeline.
    """
    message = ""
    pipeline = TrainingPipeline(config=ConfigurationManager(current_time_stamp=generate_timestamp()))
    if not TrainingPipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."

    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train_model.html', context=context)


@app.route('/predict-price', methods=['GET', 'POST'])
def predict_price():
    """
    Predict the price of a car based on user input.
    """
    context = {
        CAR_DATA_KEY: None,
        PREDICTED_PRICE_KEY: None
    }
    car_list = get_carlist()

    if request.method == "POST":
        car_name = request.form.get("car_name")
        vehicle_age = int(request.form.get("vehicle_age"))
        km_driven = int(request.form.get("km_driven"))
        seller_type = request.form.get("seller_type")
        fuel_type = request.form.get("fuel_type")
        transmission_type = request.form.get("transmission")
        mileage = float(request.form.get("mileage"))
        engine = int(request.form.get("engine"))
        max_power = float(request.form.get("max_power"))
        seats = int(request.form.get("seats"))

        car_data = CarPriceInputData(
            car_name=car_name,
            vehicle_age=vehicle_age,
            km_driven=km_driven,
            seller_type=seller_type,
            fuel_type=fuel_type,
            transmission_type=transmission_type,
            mileage=mileage,
            engine=engine,
            max_power=max_power,
            seats=seats
        )
        car_data_df = car_data.to_dataframe()
        predictor = CarPricePredictor(model_dir=SAVED_MODELS_DIR)
        predicted_price = predictor.predict(X=car_data_df)
        context = {
            CAR_DATA_KEY: car_data.to_dataframe().to_dict(orient="records")[0],
            PREDICTED_PRICE_KEY: round(predicted_price[0], 2)
        }
        return render_template('predict_price.html', context=context, car_list=car_list)

    return render_template('predict_price.html', context=context, car_list=car_list)


@app.route('/models', defaults={'requested_path': 'saved_models'})
@app.route('/models/<path:requested_path>')
def saved_models_directory(requested_path):
    """
    Render the saved models directory for browsing files.
    """
    os.makedirs("saved_models", exist_ok=True)
    absolute_path = os.path.join(requested_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(absolute_path):
        return abort(404)

    # Serve file if it's a file
    if os.path.isfile(absolute_path):
        return send_file(absolute_path)

    # Show directory contents
    files = {os.path.join(absolute_path, file): file for file in os.listdir(absolute_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(absolute_path),
        "parent_label": absolute_path
    }
    return render_template('saved_models.html', result=result)


@app.route("/update-config", methods=['GET', 'POST'])
def update_model_config():
    """
    Update the model configuration file.
    """
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            model_config = json.loads(model_config)
            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_config.html', result={"model_config": model_config})

    except Exception as e:
        logging.exception(e)
        return str(e)


@app.route('/logs', defaults={'requested_path': 'logs'})
@app.route('/logs/<path:requested_path>')
def render_logs_directory(requested_path):
    """
    Render the logs directory for browsing log files.
    """
    os.makedirs(LOGS_FOLDER_NAME, exist_ok=True)
    absolute_path = os.path.join(requested_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(absolute_path):
        return abort(404)

    # Serve file if it's a file
    if os.path.isfile(absolute_path):
        log_df = get_log_dataframe(absolute_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('logs.html', context=context)

    # Show directory contents
    files = {os.path.join(absolute_path, file): file for file in os.listdir(absolute_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(absolute_path),
        "parent_label": absolute_path
    }
    return render_template('logs_files.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)