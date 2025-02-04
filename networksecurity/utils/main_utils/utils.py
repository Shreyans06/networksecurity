import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
import numpy as np
import pickle
import dill

def read_yaml_file(file_path: str):
    try:
        with open(file_path , "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error reading yaml file {file_path}")
        raise NetworkSecurityException(e , sys)

def write_yaml_file(file_path: str , content: object , replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path) , exist_ok = True)
        with open(file_path , "w") as file:
            yaml.dump(content , file)
        
    except Exception as e:
        logging.error(f"Error writing yaml file {file_path}")
        raise NetworkSecurityException(e , sys)