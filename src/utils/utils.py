import os
import sys
import yaml
import pickle
import pymongo
import pandas as pd
from ensure import ensure_annotations
from box import ConfigBox
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier,VotingClassifier

from src.logging.logger import logging
from src.exception.exception import CustomException


@ensure_annotations
def read_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            logging.info(f'YAML file {file_path} loaded successfully')

        return ConfigBox(data)
    except Exception as e:
        logging.info(str(e))
        raise CustomException(sys, e)


def create_dir(file_path: list, verbose=True):
    try:
        for path in file_path:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")
    except Exception as e:
        raise CustomException(sys, e)


def data_from_db(url, db, collection):
    try:
        client = pymongo.MongoClient(url)

        db = client[db]
        collection = db[collection]

        data = []
        for i in collection.find():
            data.append(i)

        df = pd.DataFrame(data)

        if 'Unnamed: 0' in df.columns:
            df.drop(columns=['_id', 'Unnamed: 0'], axis=1, inplace=True)
        else:
            df.drop(columns=['_id'], axis=1, inplace=True)

        print(df.head())

        return df

    except Exception as e:
        logging.info(str(e))
        raise CustomException(sys, e)


def save_obj(file_path, obj):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def model_evaluatuion(x_train, y_train, x_test, y_test, models):

    logging.info(' model evaluation started')
    report = {}
    for name, clf in models:
        
    
        model=BaggingClassifier(estimator=clf,n_estimators=50,random_state=45,verbose=3,n_jobs=-1,oob_score=True)
       

            # Train model
        model.fit(x_train, y_train)

            # Predict Testing data
        y_test_pred = model.predict(x_test)

        test_model_score = accuracy_score(y_test, y_test_pred)*100

        report[name] = test_model_score

    return report
