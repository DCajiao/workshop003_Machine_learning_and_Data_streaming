import os
import pickle
import logging

import numpy as np
import pandas as pd

from scipy.stats import pearsonr
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_data(data):
    """
    Splits the dataset into training and testing sets with target and feature separation.

    Args:
        data (pandas.DataFrame): The input dataset containing features and target variables.

    Returns:
        dict: A dictionary containing `X_train`, `X_test`, `y_train`, and `y_test` DataFrames.
    """
    try:
        logging.info('Splitting data...')
        data = pd.get_dummies(data, columns=['Year'])
        X = data.drop(columns=['Happiness_Score', 'Happiness_Rank', 'Country'])
        Y = data['Happiness_Score']
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

        splited_data = {
            'X_train': X_train,
            'X_test': X_test,
            'y_train': y_train,
            'y_test': y_test
        }
        return splited_data
    except Exception as e:
        logging.error(f"An error occurred while splitting the data: {e}")
        raise e


def set_model(splited_data):
    """
    Creates and trains a Random Forest regression model within a pipeline.

    Args:
        splited_data (dict): The dictionary containing training and testing data.

    Returns:
        sklearn.pipeline.Pipeline: The trained pipeline model.
    """
    try:
        logging.info('Setting the model...')
        X_train = splited_data['X_train']
        y_train = splited_data['y_train']

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', RandomForestRegressor())
        ])

        pipeline.fit(X_train, y_train)
        return pipeline
    except Exception as e:
        logging.error(f"An error occurred while setting the model: {e}")
        raise e


def get_metrics(splited_data, pipeline):
    """
    Evaluates the trained model using the test dataset and computes performance metrics.

    Args:
        splited_data (dict): The dictionary containing testing data.
        pipeline (sklearn.pipeline.Pipeline): The trained pipeline model.

    Returns:
        dict: A dictionary containing R², MAE, MSE, and RMSE metrics.
    """
    try:
        logging.info('Getting metrics...')
        X_test = splited_data['X_test']
        y_test = splited_data['y_test']

        y_pred = pipeline.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        metrics = {
            'R²': r2,
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse
        }
        logging.info(f'The model has the following metrics: \n{metrics}')
        return metrics
    except Exception as e:
        logging.error(f"An error occurred while getting metrics: {e}")
        raise e


def export_model(pipeline):
    """
    Saves the trained model pipeline to a pickle file.

    Args:
        pipeline (sklearn.pipeline.Pipeline): The trained pipeline model.

    Returns:
        str: The file path where the model was saved.
    """
    try:
        logging.info('Saving the model...')
        if not os.path.exists('models'):
            os.makedirs('models')
        model_path = 'models/model.pkl'
        with open(model_path, 'wb') as file:
            pickle.dump(pipeline, file)

        logging.info(f'Model saved at {model_path}')
        return model_path
    except Exception as e:
        logging.error(f"An error occurred while saving the model: {e}")
        raise e


def train_the_model(**kwargs):
    """
    Trains a model pipeline and saves it after computing metrics.

    Args:
        **kwargs: Keyword arguments including `ti` (TaskInstance) for XCom data pulling.

    Returns:
        str: The file path where the trained model was saved.
    """
    try:
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='get_db_data')
        
        splited_data = split_data(data)
        pipeline = set_model(splited_data)
        metrics = get_metrics(splited_data, pipeline)
        model_path = export_model(pipeline)
        return model_path
    except Exception as e:
        logging.error(f"An error occurred while training the model: {e}")
        raise e

