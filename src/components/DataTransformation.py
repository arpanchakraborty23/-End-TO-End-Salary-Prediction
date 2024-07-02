import os,sys
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from src.utils.utils import save_obj
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.configure.config_manager import ConfigMnager

class DataTransformation:
    def __init__(self) -> None:
        config_manager=ConfigMnager()
        self.config=config_manager.get_data_transformation_config()

        logging.info('Data Transformation strted')

    def preprocess_obj(self):
        '''
        method: preprocess_obj
        Discripotion: This is data preprocessing pipline object automate data preprocesssing

        output: prepoecss_obj

        '''
        try:
            preprocess_obj=Pipeline(
                steps=[
                    (['Impute',SimpleImputer(strategy='median')]),
                    ('Z-score',StandardScaler())
                ]
            )

            return preprocess_obj
        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)
        
    def initate_data_transformation(self,train_data,test_data):
        '''
        method: initate_data_transformation
        Discripotion: Transform data into numpy array
        output: preprocesser.pkl

        '''
        try:
            train_df=pd.read_csv(train_data)
            test_df=pd.read_csv(test_data)
            
            if 'Unnamed: 0' in train_df.columns:
                    train_df.drop(columns=['Unnamed: 0'],axis=1,inplace=True)
             
            else:
                    train_df
            print(train_df.head())

            if 'Unnamed: 0' in test_df.columns:
                    test_df.drop(columns=['Unnamed: 0'],axis=1,inplace=True)
             
            else:
                    test_df
            print(test_df.head())

            logging.info('Data loaded')
            Target=self.config.Target
            
            # X train
            input_features_train_df=train_df.drop(columns=Target,axis=1)

            # y train
            target_feature_train_df=train_df[Target]

            # x test
            input_features_test_df=test_df.drop(columns=Target,axis=1)

            # y test
            target_feature_test_df=test_df[Target]

            ## data scaling
            obj=self.preprocess_obj()

            tranfom_data_train_df=obj.fit_transform(input_features_train_df)

            tranfom_data_test_df=obj.transform(input_features_test_df)

            logging.info(f'scale data {tranfom_data_train_df}')

            train_arr=np.c_[tranfom_data_train_df,np.array(target_feature_train_df)]
            np.save(self.config.train_arr,train_arr)

            test_arr=np.c_[tranfom_data_test_df,np.array(target_feature_test_df)]
            np.save(self.config.test_arr,test_arr)

            save_obj(
                file_path=self.config.preprocess_obj,
                obj=obj
            )

            return(
                train_arr,
                test_arr
            )

            
        except Exception as e:
            logging.info(str(e))
            raise CustomException(sys,e)