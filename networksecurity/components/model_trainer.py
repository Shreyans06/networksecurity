import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact , DataTransformationArtifact


from networksecurity.utils.main_utils.utils import save_object , load_object , load_numpy_array
from networksecurity.utils.ml_utils.evaluate.evaluate_models import evaluate_models 
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classfication_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import mlflow

class ModelTrainer:
    def __init__(self , model_trainer_config: ModelTrainerConfig , data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    def track_mlflow(self , best_model , classification_metric):
        with mlflow.start_run():
            f1 = classification_metric.f1_score
            precision = classification_metric.precision
            recall = classification_metric.recall

            mlflow.log_metric("f1_score" , f1)
            mlflow.log_metric("precision" , precision)
            mlflow.log_metric("recall_score" , recall)

            mlflow.sklearn.log_model(best_model , "model")
        

    def train_model(self , X_train , y_train , X_test , y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose = 1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }

        params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,128,256]
                }
                
            }

        model_report: dict = evaluate_models(X_train , y_train , X_test , y_test , models = models , param = params)

        best_model_score = max(sorted(model_report.values()))

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
            ]
        
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classfication_score(y_train , y_train_pred)

        ## Track the experiments with MLflow
        self.track_mlflow(best_model , classification_train_metric)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classfication_score(y_test , y_test_pred)

        ## Track the experiments with MLflow
        self.track_mlflow(best_model , classification_test_metric)

        preprocessor = load_object(file_path= self.data_transformation_artifact.transformed_object_file_path)
        # print(self.model_trainer_config.trained_model_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path , exist_ok= True)

        network_model = NetworkModel(preprocessor , best_model)
        save_object(self.model_trainer_config
                    .trained_model_file_path , network_model)
        
        model_trainer_artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path , 
                             classification_train_metric , 
                             classification_test_metric)
        
        return model_trainer_artifact

        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array(train_file_path)
            test_arr = load_numpy_array(test_file_path)

            X_train , y_train , X_test , y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_artifact = self.train_model(X_train , y_train , X_test , y_test)
            return model_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

