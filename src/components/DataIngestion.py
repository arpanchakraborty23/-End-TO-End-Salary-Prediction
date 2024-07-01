import os,sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pathlib import Path
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.logging.logger import logging
from src.exception.exception import CustomException
from src.configure.config_manager import ConfigMnager
from src.utils.utils import data_from_db


load_dotenv()
class DataIngetion:
    def __init__(self) -> None:
        config=ConfigMnager()
        self.config=config.get_data_ingetion_config()

        logging.info('Data Ingestion has started' )

    def initiate_data_ingestion(self):
        try:
            ## Data collect from MongoDB
            # df=data_from_db(url=os.getenv('url'),
            #                 db=os.getenv('db'),
            #                 collection=os.getenv('collection'))
            
            df=pd.read_csv('data//clean-data.csv')
            
            
            logging.info(f'Data shape {df.shape} , columns: {df.columns} Null values: {df.isna().sum()}')

            
            os.makedirs(os.path.dirname(self.config.train_data), exist_ok=True)
            df.to_csv(self.config.raw_data)


            # split data into test and train data 
            train_data,test_data=train_test_split(df,train_size=0.30,random_state=45)

            train_data.to_csv(self.config.train_data)

            test_data.to_csv(self.config.test_data)
            

            
            return (
                self.config.train_data,
                self.config.test_data
            )
        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)

