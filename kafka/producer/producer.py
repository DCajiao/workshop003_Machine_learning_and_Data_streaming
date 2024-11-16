from src.connections.db import DB
from json import dumps, loads
from kafka import KafkaProducer, KafkaConsumer
import pandas as pd
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = DB()


def get_db_data():
    """
    Fetches all rows from the `transformed_data` table in the database and returns them as a pandas DataFrame.

    This function establishes a connection to the database using the `DB` class, executes a SQL query
    to retrieve all data from the `transformed_data` table, and converts the result into a pandas DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the `transformed_data` table.

    Raises:
        Exception: If the database connection or query execution fails.
    """
    try:
        db = DB()
        data = db.fetch_as_dataframe('SELECT * FROM transformed_data;')
        logger.info("Data fetched successfully from the database.")
        return data
    except Exception as e:
        logger.error(
            f"An error occurred while fetching data from the database: {e}")
        raise e


def kafka_producer(row):
    """
    This function sends a message to a Kafka topic.
    Every message is a row from a DataFrame converted to a dictionary with encoding utf-8.
    Kafka-dashboard it's the channel to send the messages.
    """

    logging.info("Connecting to Kafka producer")
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['kafka-test:9092'],
    )

    # Convertir row a dict
    message = row.to_dict()
    logging.info(f"🪄 Sending message: {message}")
    producer.send('happiness-topic', value=message)
    logging.info(f"🪄 Message sent: {message}")

if __name__ == "__main__":
    time.sleep(20) # A delay to wait for the Kafka container to be ready
    data = get_db_data()
    for row in data.iterrows():
        logging.info(f"Sending data to Kafka.")
        row = row[1]
        kafka_producer(row)
        time.sleep(10)
