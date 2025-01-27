import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv
import certifi

load_dotenv()

MONOGO_DB_URL = os.getenv('MONGO_DB_URL')

certificate_authorities = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e , sys)

    def csv_to_json(self , file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True , inplace= True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def insert_data_mongodb(self , records , database , collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONOGO_DB_URL , tlsCAFile=certificate_authorities)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e , sys)


if __name__ == "__main__":
    try:
        FILE_PATH = 'Network_Data/phishingData.csv'
        DATABASE = 'Network_Security'
        collection = "network_data" 
        network_data_extract = NetworkDataExtract()
        records = network_data_extract.csv_to_json(FILE_PATH)
        inserted_records = network_data_extract.insert_data_mongodb(records , DATABASE , collection)
        logging.info(f"Inserted {inserted_records} records in MongoDB")
        print(inserted_records)
    except Exception as e:
        logging.error(f"Error in inserting data in MongoDB {e}")
        raise NetworkSecurityException(e , sys)