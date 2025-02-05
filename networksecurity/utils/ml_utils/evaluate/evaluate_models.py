from networksecurity.exception.exception import NetworkSecurityException
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import sys

def evaluate_models(X_train , y_train , X_test , y_test , models , param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            parameters = param[list(models.keys())[i]]

            gs = GridSearchCV(model , parameters , cv = 3)
            gs.fit(X_train , y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train , y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = accuracy_score(y_train , y_train_pred)

            test_model_score = accuracy_score(y_test , y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        
        return report
    except Exception as e:
        raise NetworkSecurityException(e , sys)