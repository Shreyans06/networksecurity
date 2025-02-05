import sys
import os
import numpy as np
import pandas as pd
from scipy import test
from scipy.stats import t
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import DataTransformationArtifact , DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_object , save_numpy_array

class DataTransformation:
    def __init__(self , data_validation_artifact: DataValidationArtifact , data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            logging.error("Error initializing DataTransformation object")
            raise NetworkSecurityException(e , sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error reading file {file_path}")
            raise NetworkSecurityException(e , sys)

    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Getting Data Transformer Object")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Initialized KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS} ")
            processor:Pipeline = Pipeline([("imputer" , imputer)])
            return processor
        except Exception as e:  
            logging.error("Error getting Data Transformer Object")
            raise NetworkSecurityException(e , sys)
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating Data Transformation")
        try:
            logging.info("Reading Validated Data")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training dataframe
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN] , axis = 1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1 , 0)

            ## Testing dataframe
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN] , axis = 1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1 , 0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature , np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature , np.array(target_feature_test_df)]

            save_numpy_array(self.data_transformation_config.transformed_train_file_path , train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path , test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path , preprocessor_obj)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path)
            
            return data_transformation_artifact
        except Exception as e:
            logging.error("Error initiating Data Transformation")
            raise NetworkSecurityException(e , sys)