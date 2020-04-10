import os
from datetime import datetime
from carprice.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    TrainingPipelineConfig,
)
from carprice.util.util import read_yaml_file
from carprice.logger import logging
from carprice.constant import *
from carprice.exception import CarException


class ConfigurationManager:
    """
    Configuration Manager class to handle all configuration-related operations
    for the car price prediction pipeline.
    """

    def __init__(self, config_file_path: str = CONFIG_FILE_PATH, timestamp: str = CURRENT_TIME_STAMP) -> None:
        """
        Initializes the ConfigurationManager with the provided configuration file path and timestamp.

        Args:
            config_file_path (str): Path to the configuration YAML file.
            timestamp (str): Current timestamp for organizing artifacts.
        """
        try:
            self.config_data = read_yaml_file(file_path=config_file_path)
            self.pipeline_config = self._get_training_pipeline_config()
            self.timestamp = timestamp
        except Exception as e:
            raise CarException(e, sys) from e

    def _get_training_pipeline_config(self) -> TrainingPipelineConfig:
        """
        Retrieves the training pipeline configuration.

        Returns:
            TrainingPipelineConfig: Configuration object for the training pipeline.
        """
        try:
            pipeline_config = self.config_data[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_directory = os.path.join(
                ROOT_DIR,
                pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY],
            )
            pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_directory)
            logging.info(f"Training Pipeline Config: {pipeline_config}")
            return pipeline_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Retrieves the data ingestion configuration.

        Returns:
            DataIngestionConfig: Configuration object for data ingestion.
        """
        try:
            artifact_dir = self.pipeline_config.artifact_dir
            ingestion_artifact_dir = os.path.join(
                artifact_dir, DATA_INGESTION_ARTIFACT_DIR, self.timestamp
            )
            ingestion_info = self.config_data[DATA_INGESTION_CONFIG_KEY]

            bucket_name = ingestion_info[S3_BUCKET_NAME_KEY]
            object_name = ingestion_info[S3_OBJECT_NAME_KEY]
            local_file_name = ingestion_info[LOCAL_FILE_NAME_KEY]

            raw_data_dir = os.path.join(
                ingestion_artifact_dir, ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )
            ingested_data_dir = os.path.join(
                ingestion_artifact_dir, ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            train_dir = os.path.join(ingested_data_dir, ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
            test_dir = os.path.join(ingested_data_dir, ingestion_info[DATA_INGESTION_TEST_DIR_KEY])

            data_ingestion_config = DataIngestionConfig(
                bucket_name=bucket_name,
                object_name=object_name,
                local_file_name=local_file_name,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=train_dir,
                ingested_test_dir=test_dir,
            )
            logging.info(f"Data Ingestion Config: {data_ingestion_config}")
            return data_ingestion_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Retrieves the data validation configuration.

        Returns:
            DataValidationConfig: Configuration object for data validation.
        """
        try:
            artifact_dir = self.pipeline_config.artifact_dir
            validation_artifact_dir = os.path.join(
                artifact_dir, DATA_VALIDATION_ARTIFACT_DIR_NAME, self.timestamp
            )
            validation_info = self.config_data[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path = os.path.join(
                ROOT_DIR,
                validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY],
            )
            report_file_path = os.path.join(
                validation_artifact_dir, validation_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )
            report_page_file_path = os.path.join(
                validation_artifact_dir, validation_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
            )
            logging.info(f"Data Validation Config: {data_validation_config}")
            return data_validation_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Retrieves the data transformation configuration.

        Returns:
            DataTransformationConfig: Configuration object for data transformation.
        """
        try:
            artifact_dir = self.pipeline_config.artifact_dir
            transformation_artifact_dir = os.path.join(
                artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR, self.timestamp
            )
            transformation_info = self.config_data[DATA_TRANSFORMATION_CONFIG_KEY]

            preprocessing_file_path = os.path.join(
                transformation_artifact_dir,
                transformation_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],
                transformation_info[DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY],
            )
            transformed_train_dir = os.path.join(
                transformation_artifact_dir,
                transformation_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                transformation_info[DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY],
            )
            transformed_test_dir = os.path.join(
                transformation_artifact_dir,
                transformation_info[DATA_TRANSFORMATION_DIR_NAME_KEY],
                transformation_info[DATA_TRANSFORMATION_TEST_DIR_NAME_KEY],
            )

            data_transformation_config = DataTransformationConfig(
                preprocessed_object_file_path=preprocessing_file_path,
                transformed_train_dir=transformed_train_dir,
                transformed_test_dir=transformed_test_dir,
            )
            logging.info(f"Data Transformation Config: {data_transformation_config}")
            return data_transformation_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Retrieves the model trainer configuration.

        Returns:
            ModelTrainerConfig: Configuration object for model training.
        """
        try:
            artifact_dir = self.pipeline_config.artifact_dir
            trainer_artifact_dir = os.path.join(
                artifact_dir, MODEL_TRAINER_ARTIFACT_DIR, self.timestamp
            )
            trainer_info = self.config_data[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path = os.path.join(
                trainer_artifact_dir,
                trainer_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
                trainer_info[MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY],
            )
            model_config_file_path = os.path.join(
                trainer_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
                trainer_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY],
            )
            base_accuracy = trainer_info[MODEL_TRAINER_BASE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path,
            )
            logging.info(f"Model Trainer Config: {model_trainer_config}")
            return model_trainer_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        """
        Retrieves the model evaluation configuration.

        Returns:
            ModelEvaluationConfig: Configuration object for model evaluation.
        """
        try:
            evaluation_info = self.config_data[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir = os.path.join(
                self.pipeline_config.artifact_dir, MODEL_EVALUATION_ARTIFACT_DIR
            )
            evaluation_file_path = os.path.join(
                artifact_dir, evaluation_info[MODEL_EVALUATION_FILE_NAME_KEY]
            )

            model_evaluation_config = ModelEvaluationConfig(
                model_evaluation_file_path=evaluation_file_path, time_stamp=self.timestamp
            )
            logging.info(f"Model Evaluation Config: {model_evaluation_config}")
            return model_evaluation_config
        except Exception as e:
            raise CarException(e, sys) from e

    def get_model_pusher_config(self) -> ModelPusherConfig:
        """
        Retrieves the model pusher configuration.

        Returns:
            ModelPusherConfig: Configuration object for model pushing.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pusher_info = self.config_data[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path = os.path.join(
                ROOT_DIR, pusher_info[MODEL_PUSHER_MODEL_EXPORT_DIR_KEY], timestamp
            )

            model_pusher_config = ModelPusherConfig(export_dir_path=export_dir_path)
            logging.info(f"Model Pusher Config: {model_pusher_config}")
            return model_pusher_config
        except Exception as e:
            raise CarException(e, sys) from e