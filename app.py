from flask import Flask, render_template, request, send_file
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.pipline.prediction_pipline import PredictionPipeline
from src.configure.config_manager import ConfigMnager
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        config = ConfigMnager()
        pred_config = config.get_prediction_config()

        logging.info('Prediction started')
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline()
            prediction_pipeline.run_pipeline()

            logging.info('Prediction Completed. Download file.')

            return send_file(prediction_pipeline.prediction_file_path,
                             download_name=pred_config.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload.html')

    except Exception as e:
        logging.error(f'Error in bulk app prediction: {str(e)}')
        raise CustomException(sys, e) from e 

if __name__ == "__main__":
    app.run(debug=True, port=5000)
