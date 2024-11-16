import requests
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = 'https://happiness-score-prediction-api.onrender.com/upload_model'


def upload_model_file(**kwargs):
    """
    Uploads a trained model file to the API endpoint for deployment.

    This function retrieves the file path of the trained model from XCom,
    reads the file in binary mode, and sends it as a POST request to the API.

    Args:
        **kwargs: Keyword arguments, including `ti` (TaskInstance) to pull data from XCom.

    Returns:
        dict: The JSON response from the API.
    """
    try:
        ti = kwargs['ti']
        model_path = ti.xcom_pull(task_ids='train_model')
        logger.info(f"Uploading model file: {model_path}")
        
        with open(model_path, 'rb') as file:
            files = {'model': file}
            response = requests.post(API_URL, files=files)

        if response.status_code == 200:
            logger.info("Model uploaded successfully.")
            return response.json()
        else:
            logger.info(f"Failed to upload model. Status code: {response.status_code}")
            print(f"Failed to upload model. Status code: {response.status_code}")
            return response.json()
    except Exception as e:
        logger.error(f"An error occurred while uploading the model: {e}")
        raise e
