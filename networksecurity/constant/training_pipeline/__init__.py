import os
import sys
import numpy as np
import pandas as pd

"""
TRAINING PIPELINE CONSTANTS DEFINITION
"""

TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"
"""
DATA SCHEMA CONSTANTS DEFINITION
"""
SCHEMA_FILE_PATH: str = os.path.join("data_schema" , "schema.yaml")


SAVED_MODEL_DIR: str = "saved_models"
MODEL_FILE_NAME: str = "model.pkl"


"""
DATA INGESTION CONSTANTS DEFINITION
"""
DATA_INGESTION_COLLECTION_NAME: str = "network_data"
DATA_INGESTION_DATABSE_NAME: str = "Network_Security"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
DATA VALIDATION CONSTANTS DEFINITION
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"


"""
DATA TRANSFORMATION CONSTANTS DEFINITION
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

# KNN Inmputer to replace NaN values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 5,
    "weights": "uniform",
}

DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

"""
MODEL TRAINING CONSTANTS DEFINITION
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_THRESHOLD: float = 0.05

"""
PREDICTION CONSTANTS DEFINITION
"""
FINAL_MODEL_DIR_NAME: str = "final_model"
FINAL_MODEL_FILE_NAME: str = "model.pkl"
FINAL_PREPROCESSOR_FILE_NAME: str = "preprocessor.pkl"

"""
AWS CONSTANTS
"""
TRAINING_BUCKET_NAME = "phishingsecurity"

