import os
import pickle
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManagement:
    def __init__(self, model_path):
        """
        Initialize the ModelManagement class by loading a specified model.

        Args:
            model_path (str): Path to the initial model file.
        """
        self.model = None
        self.model_path = model_path
        self.load_model(model_path)

    def load_model(self, model_path):
        """
        Load a model from a pickle file and set it as the current model.

        Args:
            model_path (str): Path to the model file.

        Raises:
            FileNotFoundError: If the specified model file does not exist.
        """
        if not os.path.exists(model_path):
            logger.error(f"Model file not found at {model_path}")
            raise FileNotFoundError(f"Model file not found at {model_path}")

        try:
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
            self.model_path = model_path
            logger.info(f"Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def predict(self, input_df):
        """
        Generate a single prediction using the loaded model.

        Args:
            input_df (pd.DataFrame): DataFrame containing input features (one row).

        Returns:
            float: Prediction value.

        Raises:
            ValueError: If no model is loaded or if the input DataFrame is empty.
        """
        if self.model is None:
            raise ValueError("No model is currently loaded.")

        if input_df.empty:
            raise ValueError("Input DataFrame is empty.")

        try:
            # Generate prediction
            prediction = self.model.predict(input_df)[0]
            logger.info(f"Prediction generated: {prediction}")
            return prediction
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

    def show_models(self):
        """
        Show all available models in the models directory and mark the currently loaded model.

        Returns:
            list: List of model file paths.
        """
        # model_files = [name for name in os.listdir('./models') if name.endswith('_happiness_score_prediction_model.pkl')]
        model_files = os.listdir('./models')
        logger.info(f"Available models: {model_files}")
        return model_files
