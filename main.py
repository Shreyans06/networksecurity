from networksecurity.components import data_transformation, data_validation, model_trainer
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, ModelTrainerConfig , TrainingPipelineConfig , DataValidationConfig , DataTransformationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data Ingestion Object Created")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact , data_validation_config)
        logging.info("Data Validation Object Created")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)
        
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact , data_transformation_config)
        logging.info("Data Transformation Object Created")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = model_trainer.ModelTrainer(model_trainer_config , data_transformation_artifact)
        logging.info("Model trainer Object created")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model Training completed")
        print(model_trainer_artifact)

    except Exception as e:
        raise NetworkSecurityException(e , sys) 