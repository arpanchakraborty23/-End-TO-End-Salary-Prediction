import os,sys
import yaml
import pymongo
import pandas as pd
from ensure import ensure_annotations
from box import ConfigBox

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
        raise CustomException(sys,e)
    


def create_dir(file_path:list,verbose=True):
    try:
        for path in file_path:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")    
    except Exception as e:
        raise CustomException(sys,e)

def data_from_db(url,db,collection):
    try:
        client=pymongo.MongoClient(url)

        db=client[db]
        collection=db[collection]

        data=[]
        for i in collection.find():
            data.append(i)

        df=pd.DataFrame(data)

        df.drop(columns=['_id','Unnamed: 0'],axis=1,inplace=True)

        print(df.head())

        return df



    except Exception as e:
        logging.info(str(e))
        raise CustomException(sys,e)