import sys
import os

import certifi

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")

import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , File , UploadFile , Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABSE_NAME
from networksecurity.constant.training_pipeline import FINAL_MODEL_DIR_NAME , FINAL_MODEL_FILE_NAME , FINAL_PREPROCESSOR_FILE_NAME

from pymongo.mongo_client import MongoClient

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

client = MongoClient(mongo_db_url , tlsCAFile = ca)

database = client[DATA_INGESTION_DATABSE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins = ["*"]

app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
)

@app.get("/" , tags = ["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e , sys)
    
@app.get("/predict")
async def predict_route(request: Request , file: UploadFile = File(...)):
    try:
        model_file_loc = os.path.join(FINAL_MODEL_DIR_NAME , FINAL_MODEL_FILE_NAME)
        preprocessor_file_loc = os.path.join(FINAL_MODEL_DIR_NAME , FINAL_PREPROCESSOR_FILE_NAME)

        preprocessor = load_object(preprocessor_file_loc)
        model = load_object(model_file_loc)

        network_model = NetworkModel(preprocessor= preprocessor , model= model)
        df = pd.read_csv(file.file)
        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)

        df['predicted_column'] = y_pred
        print(df['predicted_column'])

        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html" , {"request" : request , "table" : table_html})
    except Exception as e:
        raise NetworkSecurityException(e , sys)


if __name__ == "__main__":
    app_run(app , host = "localhost" , port = 8000)