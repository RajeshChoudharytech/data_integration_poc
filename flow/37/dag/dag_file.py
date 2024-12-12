
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.s3_key_sensor import S3KeySensor
from airflow.providers.amazon.aws.transfers.sftp_to_s3 import SFTPToS3Operator
from datetime import datetime

# Create the DAG
with DAG(
    'dynamic_dag',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 1, 1),
        'retries': 1
    },
    schedule_interval='@hourly'
) as dag:
    starts = BashOperator(
        task_id='starts',
        bash_command="echo start"
    )
    process = BashOperator(
        task_id='process',
        bash_command="echo process"
    )
    end = BashOperator(
        task_id='end',
        bash_command="echo end"
    )
    start >> process
    process >> end
