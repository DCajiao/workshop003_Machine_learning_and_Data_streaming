import os
import pandas as pd
import logging
import markdown

from flask import Flask, request, jsonify

from core.model_management import ModelManagement

############ BASIC CONFIGURATION ############
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Path to the initial model
MODEL_PATH = './models/00_happiness_score_prediction_model.pkl'

# Initialize the ModelManagement instance
try:
    model_manager = ModelManagement(MODEL_PATH)
except Exception as e:
    logger.error(f"Failed to initialize ModelManagement: {e}")


@app.route('/', methods=['GET'])
def get_docs():
    """
    Return the content of the README.md file for documentation.

    Returns:
        str: Content of README.md file.
    """
    try:
        with open('./methods.md', 'r') as readme_file:
            content = readme_file.read()
            logger.info("Documentation retrieved successfully.")
            html = markdown.markdown(content)
            return html
    except FileNotFoundError:
        logger.error("README.md file not found.")
        return "README.md file not found.", 404
    except Exception as e:
        logger.error(f"Unexpected error retrieving documentation: {e}")
        return "Error retrieving documentation.", 500


@app.route('/upload_model', methods=['POST'])
def upload_model():
    """
    Upload a new model file and load it into the API.

    Returns:
        dict: Confirmation message and new model path.
    """
    try:
        if 'model' not in request.files:
            logger.error("No model file provided in the request.")
            return jsonify({"error": "No model file provided."}), 400

        model_file = request.files['model']

        # Determine the new model path with autoincrement
        model_count = len([name for name in os.listdir('./models') if name.endswith('_happiness_score_prediction_model.pkl')])
        model_count = str(model_count).zfill(2)
        new_model_path = f"./models/{model_count}_happiness_score_prediction_model.pkl"

        # Save the new model file
        model_file.save(new_model_path)
        logger.info(f"Model file saved at {new_model_path}")

        # Load the new model
        model_manager.load_model(new_model_path)

        logger.info(f"New model uploaded and loaded from {new_model_path}.")
        return jsonify({"message": "New model uploaded and loaded successfully.", "model_path": new_model_path}), 200
    except Exception as e:
        logger.error(f"Error uploading and loading new model: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict endpoint that receives input features and returns a single prediction value.

    Returns:
        dict: Prediction value in JSON format.
    """
    try:
        input_data = request.get_json()
        if input_data is None:
            logger.error("Invalid JSON input received.")
            return jsonify({"error": "Invalid JSON input."}), 400

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])

        # Get prediction
        prediction = model_manager.predict(input_df)

        return jsonify({"prediction": prediction})
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/models', methods=['GET'])
def show_models():
    """
    Show all available models in the models directory and mark the currently loaded model.

    Returns:
        dict: List of model file paths.
    """
    try:
        model_files = model_manager.show_models()
        return jsonify({"models": model_files}), 200
    except Exception as e:
        logger.error(f"Error showing models: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
