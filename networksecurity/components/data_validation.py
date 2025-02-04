from tkinter.tix import STATUS
from numpy import test
from networksecurity.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file , write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys


class DataValidation:
    def __init__(self , data_ingestion_artifact: DataIngestionArtifact , data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.__schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e , sys) 

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def validate_num_of_columns(self , df: pd.DataFrame) -> bool:
        try:
            true_columns = len(self.__schema_config["columns"])
            df_columns = len(df.columns)
            logging.info(f"Number of columns in the schema: {true_columns}")
            logging.info(f"Number of columns in the data: {df_columns}")
            if true_columns == df_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def detect_dataset_drift(self , base_df , current_df , threshold = 0.05) -> bool:
        try:
            drift_status = False
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                statistic , p_value = ks_2samp(d1 , d2)

                logging.info(f"Column: {column} , statistic: {statistic} , p_value: {p_value}")
                if p_value < threshold:
                    drift_status = True
                    logging.info(f"Drift detected in column: {column}")
                
                report.update({column : {"p_value" : float(p_value) , "drift_status" : drift_status}})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path , exist_ok=True)
            write_yaml_file(drift_report_file_path , report , replace=False)
            return True
        except Exception as e:
            raise NetworkSecurityException(e , sys)

    def initiate_data_validation(self) -> DataIngestionArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read the data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            ## Validate the data
            train_status = self.validate_num_of_columns(train_df)
            if not train_status:
                error_message = "Number of columns in the train data is not same as the schema"
            
            test_status = self.validate_num_of_columns(test_df)
            if not test_status:
                error_message = "Number of columns in the test data is not same as the schema"

            ## Check data drift
            dft_status = self.detect_dataset_drift(train_df , test_df)
            
            dir_name = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_name , exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path , index=False , header=True)

            test_df.to_csv(self.data_validation_config.valid_test_file_path , index=False , header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status = dft_status,
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = None , 
                invalid_test_file_path = None , 
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e , sys)