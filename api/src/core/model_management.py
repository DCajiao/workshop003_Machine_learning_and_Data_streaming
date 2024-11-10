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
        try:
            self.load_model(model_path)
        except Exception as e:
            logger.error(f"Failed to load initial model: {e}")
            raise

    def load_model(self, model_path):
        """
        Load a model from a pickle file.

        Args:
            model_path (str): Path to the model file.

        Raises:
            FileNotFoundError: If the specified model file does not exist.
        """
        try:
            if not os.path.exists(model_path):
                logger.error(f"Model file not found at {model_path}")
                raise FileNotFoundError(
                    f"Model file not found at {model_path}")
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
                logger.info(f"Model loaded successfully from {model_path}")
        except FileNotFoundError as fnf_error:
            logger.error(f"FileNotFoundError: {fnf_error}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def load_new_model(self, new_model_path):
        """
        Load a new model from the specified file and replace the current model.

        Args:
            new_model_path (str): Path to the new model file.
        """
        try:
            self.load_model(new_model_path)
            self.model_path = new_model_path
            logger.info(f"New model loaded from {new_model_path}")
        except Exception as e:
            logger.error(f"Failed to load new model: {e}")
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
        try:
            if self.model is None:
                logger.error("No model is currently loaded for predictions.")
                raise ValueError("No model is currently loaded.")
            
            if input_df.empty:
                logger.error("Input DataFrame is empty.")
                raise ValueError("Input DataFrame is empty.")
            
            # Generate prediction
            prediction = self.model.predict(input_df)[0]  # Extract the first (and only) prediction
            logger.info(f"Prediction successfully generated: {prediction}")
            return prediction
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
