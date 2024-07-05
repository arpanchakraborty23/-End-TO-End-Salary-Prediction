import os,sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from xgboost import XGBClassifier

from src.configure.config_manager import ConfigMnager
from src.utils.utils import model_evaluatuion,save_obj
from src.logging.logger import logging
from src.exception.exception import CustomException

class ModelTrain:
    def __init__(self) -> None:
       config=ConfigMnager()
       self.config=config.get_model_trainer_config()

    def initate_model_train(self):
        try:
            train_array=np.load(self.config.train_arr)
            test_array=np.load(self.config.test_arr)

            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models=[
                ('LogisticRegression',LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.6)),
                ('DecisionTreeClassifier',DecisionTreeClassifier()),
                ('XGBClassifier',XGBClassifier()),
                ('KNeighborsClassifier',KNeighborsClassifier()),
                ('RandomForestClassifier',RandomForestClassifier(criterion='log_loss'))
            ]
         
            report:dict=model_evaluatuion(x_train,y_train,x_test,y_test,models)

            print(report)
            logging.info(f'Model Report : {report}')

            print('\n====================================================================================\n')

            # 6. Find the best model
            best_model_score=max(sorted(report.values()))

            
            best_model_name = list(report.keys())[
                list(report.values()).index(best_model_score)
            ]

            best_model = dict(models)[best_model_name]

            logging.info(f'Best Model Found , Model Name : {best_model_name} , Score : {best_model_score}')

            print(f'Best Model Found , Model Name : {best_model_name} , Score : {best_model_score}')
            print('\n====================================================================================\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , Score : {best_model_score}')


            save_obj(
                file_path=self.config.model,
                obj=best_model
            )
            return self.config.model
            
        except CustomException as e:
            logging.info(f'Error cooured {str(e)}')
            raise CustomException(sys,e)  