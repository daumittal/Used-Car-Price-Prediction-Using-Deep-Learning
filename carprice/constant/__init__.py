import os
from datetime import datetime


def generate_timestamp() -> str:
    """
    Generates a timestamp in the format 'YYYY-MM-DD-HH-MM-SS'.

    Returns:
        str: Current timestamp as a string.
    """
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


# Root Directory Configuration
ROOT_DIRECTORY = os.getcwd()  # Current working directory
CONFIG_DIRECTORY = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIRECTORY, CONFIG_DIRECTORY, CONFIG_FILE_NAME)

CURRENT_TIMESTAMP = generate_timestamp()


# Training Pipeline Configuration Keys
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


# Data Ingestion Configuration Keys
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_BUCKET_NAME_KEY = "bucket_name"
DATA_INGESTION_OBJECT_NAME_KEY = "object_name"
DATA_INGESTION_LOCAL_FILE_NAME_KEY = "local_file_name"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_INGESTED_DIR_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"


# Data Validation Configuration Keys
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_ARTIFACT_DIR = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"


# Data Transformation Configuration Keys
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"


# Dataset Schema Keys
DATASET_SCHEMA_COLUMNS_KEY = "columns"
NUMERICAL_COLUMNS_KEY = "numerical_columns"
CATEGORICAL_COLUMNS_KEY = "categorical_columns"
ONEHOT_COLUMNS_KEY = "onehot_columns"
BINARY_COLUMNS_KEY = "binary_columns"
TARGET_COLUMN_KEY = "target_column"


# Model Training Configuration Keys
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"


# Model Evaluation Configuration Keys
MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"


# Model Pusher Configuration Keys
MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = "model_export_dir"


# Experiment Tracking Keys
BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

EXPERIMENT_DIR_NAME = "experiment"
EXPERIMENT_FILE_NAME = "experiment.csv"