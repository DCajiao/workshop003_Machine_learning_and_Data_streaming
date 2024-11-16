import requests
import json
import logging
import time

from json import dumps, loads
from kafka import KafkaConsumer
import pandas as pd
import logging

import pandas as pd
from src.connections.db import DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = 'https://happiness-score-prediction-api.onrender.com/predict'

db = DB()


def kafka_consumer():
    """
    This function consumes messages from a Kafka topic and inserts them into a PostgreSQL database.
    """
    logging.info("🪄Connecting to Kafka consumer")
    consumer = KafkaConsumer(
        'happiness-topic',  # Topic name
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(
            m.decode('utf-8')),  # Deserialize messages to JSON
        bootstrap_servers=['kafka-test:9092']
    )

    # Consuming messages and inserting them into the database
    for message in consumer:
        logging.info(f"🪄Received message: {message.value}")
        # Convert the message to a DataFrame
        data = pd.json_normalize(data=message.value)
        year_value = data['Year'].iloc[0]
        data = pd.get_dummies(data, columns=['Year'])

        body_to_post = {
            "GDP_per_capita": data["GDP_per_capita"],
            "Social_support": data["Social_support"],
            "Health_(Life_Expectancy)": data["Health_(Life_Expectancy)"],
            "Freedom": data["Freedom"],
            "Generosity": data["Generosity"],
            "Perceptions_of_corruption": data["Perceptions_of_corruption"],
            "Year_2015": data["Year_2015"] if "Year_2015" in data.columns else False,
            "Year_2016": data["Year_2016"] if "Year_2016" in data.columns else False,
            "Year_2017": data["Year_2017"] if "Year_2017" in data.columns else False,
            "Year_2018": data["Year_2018"] if "Year_2018" in data.columns else False,
            "Year_2019": data["Year_2019"] if "Year_2019" in data.columns else False,
        }
        body_to_post = pd.DataFrame(body_to_post).to_dict(orient='records')[0]

        # Make a POST request to the API
        logger.info("🪄Making a POST request to the API prediction")
        response = requests.post(API_URL, json=body_to_post)
        response = response.json()
        if 'prediction' not in response:
            logging.error(f"🪄 API error: {response}")
            continue

        # Insert the prediction into the database
        query = f"""
        INSERT INTO predicted_data ("Happiness_Rank", "Country", "Happiness_Score", "GDP_per_capita", "Social_support", 
            "Health_(Life_Expectancy)", "Freedom", "Generosity", "Perceptions_of_corruption", "Year", "Predict_Happiness_Score") 
        VALUES ({data["Happiness_Rank"].iloc[0]},'{data["Country"].iloc[0]}', {data["Happiness_Score"].iloc[0]},{data["GDP_per_capita"].iloc[0]},
            {data["Social_support"].iloc[0]},{data["Health_(Life_Expectancy)"].iloc[0]},{data["Freedom"].iloc[0]},{data["Generosity"].iloc[0]},
            {data["Perceptions_of_corruption"].iloc[0]},{year_value},{response['prediction']});"""

        db.execute_query(query,fetch_results=False)
        logging.info("🪄Data inserted into the predicted_data table")


if __name__ == "__main__":
    time.sleep(22) # A delay to wait for the Kafka producer to start
    kafka_consumer()