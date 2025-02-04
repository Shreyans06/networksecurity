from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from networksecurity.entity.artifact_entity import DataIngestionArtifact

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self , data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e , sys)

    def export_collection_as_df(self):
        try:
            databse_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[databse_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns = ["_id"] , inplace = True)
            
            df.replace({"na" : np.nan} , inplace = True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e , sys)


    def export_data_into_feature_store(self , dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path , exist_ok= True)

            dataframe.to_csv(feature_store_file_path , index = False , header = True)

            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def split_data_into_train_test(self , dataframe: pd.DataFrame):
        try:
            train_set , test_set = train_test_split(dataframe , test_size= self.data_ingestion_config.train_test_dplit_ratio)
            logging.info("Data split into train and test set")
            logging.info(f"Train set shape: {train_set.shape}")
            logging.info(f"Test set shape: {test_set.shape}")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path , exist_ok= True)

            train_set.to_csv(self.data_ingestion_config.training_file_path , index = False , header = True)
            test_set.to_csv(self.data_ingestion_config.test_file_path , index = False , header = True)
            logging.info(f"Train set saved at {self.data_ingestion_config.training_file_path}")
            logging.info(f"Test set saved at {self.data_ingestion_config.test_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_df()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_into_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path = self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )

            return data_ingestion_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e , sys)