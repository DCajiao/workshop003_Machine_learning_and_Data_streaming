from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import  timedelta

import extract_functions as extract
import training_functions as train
import load_functions as load


# Set the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date':days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Create the DAG
dag = DAG(
    'Training_pipeline_and_automatic_model_availability',
    default_args=default_args,
    description='DAG to train a model and make it available for predictions in the API',
    tags=['happiness_score_prediction'],
)

get_db_data = PythonOperator(
    task_id='get_db_data',
    python_callable=extract.get_db_data,
    dag=dag
)

train_and_export_model = PythonOperator(
    task_id='train_model',
    python_callable=train.train_the_model,
    provide_context=True,
    dag=dag
)

upload_model = PythonOperator(
    task_id='upload_model',
    python_callable=load.upload_model_file,
    provide_context=True,
    dag=dag
)

# Set the task dependencies
get_db_data >> train_and_export_model >> upload_model
