import logging
from src.connections.db import DB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.error(f"An error occurred while fetching data from the database: {e}")
        raise e