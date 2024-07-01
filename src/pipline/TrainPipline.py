import sys
from src.components.DataIngestion import DataIngetion
from src.exception.exception import CustomException
from src.logging.logger import logging

class TrainPipline:
    def __init__(self) -> None:
        logging.info('************* Train Pipline*************')

    def pipline(self):
        try:
            logging.info('============== Data Ingestion================')
            obj=DataIngetion()
            train_data,test_data=obj.initiate_data_ingestion()

            logging.info('============== Data Ingestion completed ================')

        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)
