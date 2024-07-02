import sys
from src.components.DataIngestion import DataIngetion
from src.components.DataTransformation import DataTransformation
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

            logging.info('============== Data Transformation ================')
            transormation=DataTransformation()
            train_arr,test_arr=transormation.initate_data_transformation(train_data=train_data,test_data=test_data)

            logging.info('============== Data Transformation Completed ================')

        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)
if __name__=="__main__":
    obj=TrainPipline()
    obj.pipline()