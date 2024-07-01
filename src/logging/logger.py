import os,sys
import logging
from datetime import datetime
from src.exception.exception import CustomException

# file format
LOG_FILE_PATH =F"{datetime.now().strftime('%H_%M_%S_%d_%m_%Y')}.log"

# logging folder
logs_file_path=os.path.join(os.getcwd(),'logs',LOG_FILE_PATH)

# create log dir
os.makedirs(logs_file_path,exist_ok=True)

# marge file path
LOG_FILE=os.path.join(logs_file_path,LOG_FILE_PATH)

logging.basicConfig(
    filename=LOG_FILE,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )

if __name__=="__main__":
    logging.info('Logging has started')
   