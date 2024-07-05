import os
import sys
import pickle
from flask import request
import pandas as pd
from src.utils.utils import load_obj
from src.logging.logger import logging
from src.exception.exception import CustomException
from src.configure.config_manager import ConfigMnager
from src.entity.entity import PredictionConfig

class PredictionPipeline:
    def __init__(self, config=ConfigMnager()) -> None:
        self.config = config.get_prediction_config()
        self.prediction_file_path = os.path.join(self.config.prediction_output_dirname, self.config.prediction_file_name)

    def save_input_file(self):
        prediction_file_dir = 'prediction_artifacts'
        os.makedirs(prediction_file_dir, exist_ok=True)
        input_csv_file = request.files['file']
        pred_file_path = os.path.join(prediction_file_dir, input_csv_file.filename)
        input_csv_file.save(pred_file_path)
        return pred_file_path
    
    def predict(self, features):
        try:
            model = load_obj(self.config.model)
            scaler = load_obj(self.config.preprocess_obj)


            transform = scaler.transform(features)
            logging.info(str(transform))
            pred = model.predict(transform)
            return pred
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise CustomException(sys, e)
    
    def get_pred_as_df(self, input_csv):
        try:
            input_df = pd.read_csv(input_csv)
            drop_cols = ['Unnamed: 0']
            Target_col = 'salary'
            logging.info(f'Initial input dataframe: {input_df.head()}')
            
            input_df = input_df.drop(columns=[Target_col], axis=1)
            input_df = input_df.drop(drop_cols, axis=1)
            logging.info(f'x_test dataframe: {input_df.head()}')

            prediction = self.predict(input_df)

            input_df['Target'] = prediction
            input_df['Target'] = input_df['Target'].map({0: '<=50K', 1: '>50K'})
            
            os.makedirs(self.config.prediction_output_dirname, exist_ok=True)
            input_df.to_csv(self.prediction_file_path, index=False)
            logging.info(f"Predictions saved to {self.prediction_file_path}")
        except Exception as e:
            logging.error(f"Error during processing input dataframe: {e}")
            raise CustomException(sys, e)

    def run_pipeline(self):
        try:
            input_csv = self.save_input_file()
            self.get_pred_as_df(input_csv)
            return self.config
        except Exception as e:
            logging.error(f"Error running pipeline: {e}")
            raise CustomException(sys, e)
