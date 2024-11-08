import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()


def get_database_credentials():
    """
    Retrieve database credentials from environment variables.

    This function loads database credentials stored in environment variables 
    and returns them in a dictionary format. The environment variables should 
    be set in a `.env` file or directly in the system environment.

    Returns:
        dict: A dictionary containing the following database connection parameters:
            - 'dbname' (str or None): The name of the database.
            - 'user' (str or None): The username to connect to the database.
            - 'password' (str or None): The password for the database user.
            - 'host' (str or None): The host address of the database server.
            - 'port' (str or None): The port number on which the database server is running.
    """
    try:
        credentials = {
            'dbname': os.environ['DBNAME'],
            'user': os.environ['DBUSER'],
            'password': os.environ['DBPASS'],
            'host': os.environ['DBHOST'],
            'port': os.environ['DBPORT']
        }
        logging.info("Database credentials loaded successfully.")
        return credentials
    except KeyError as e:
        logging.error(f"Error loading database credentials: {e}")
        return None
