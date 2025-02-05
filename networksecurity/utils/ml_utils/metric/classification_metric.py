from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score , precision_score , recall_score
import sys


def get_classfication_score(y_true: list , y_pred: list) -> ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true , y_pred)
        precision = precision_score(y_true , y_pred)
        recall = recall_score(y_true , y_pred)

        classification_metric = ClassificationMetricArtifact(f1 , precision , recall)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e , sys)