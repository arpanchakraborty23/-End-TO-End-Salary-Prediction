from src.logging.logger import logging
from src.exception.exception import CustomException
from src.constant.ymal_path import config_file_path,parsms_file_path
from src.utils.utils import read_yaml,create_dir
from entity.entity import DataIngestionCongfig,DataTransformationConfig,ModelTrainConfig,PredictionConfig

import os,sys


class ConfigMnager:
    def __init__(self) -> None:

        self.config=read_yaml(config_file_path)
        self.parms=read_yaml(parsms_file_path)

        create_dir([self.config.artifacts_root])

    def get_data_ingetion_config(self):
        try:
            self.i_config=self.config.Data_ingestion

            data_ingestion_config=DataIngestionCongfig(
                dir=self.i_config.dir,
                raw_data=self.i_config.raw_data,
                train_data=self.i_config.train_data,
                test_data=self.i_config.test_data
            )

            return data_ingestion_config
        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)

    def get_data_transformation_config(self):
        try:
            config=self.config.Data_Trnsformation
            create_dir([config.dir])

            data_transformation_config=DataTransformationConfig(
                dir=config.dir,
                train_arr=config.train_arr,
                test_arr=config.test_arr,
                Target=self.parms.Target,
                train_data=config.train_data,
                test_data=config.test_data,
                preprocess_obj=config.preprocess_obj

            )
            return data_transformation_config
           

        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)

    def get_model_trainer_config(self):
        try:
            config=self.config.Model_Train
            create_dir([config.dir])

            model_train_config=ModelTrainConfig(
                dir=config.dir,
                train_arr=config.train_arr,
                test_arr=config.test_arr,
                model=config.model

            )
            return model_train_config

        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)
        
    def get_prediction_config(self):
        try:

            config=self.config.Prediction_pipline
            

            data_transformation_config=PredictionConfig(
                model=config.model,
                preprocess_obj=config.preprocess_obj,
                prediction_file_name=config.prediction_file_name,
                prediction_output_dirname=config.prediction_output_dirname
            )
            return data_transformation_config
        except Exception as e:
            logging.info(f'error {str(e)}')
            raise CustomException(sys,e)

    
    