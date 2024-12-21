
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator, EmrTerminateJobFlowOperator, EmrAddStepsOperator
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor
from airflow.operators.email import EmailOperator
from datetime import datetime

# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

# Create the DAG
with DAG(
    'generated_dynamic_dag',
    default_args=default_args,
    schedule_interval=None
) as dag:

    sensor_simplehttpoperator_985a45e2a = SimpleHttpOperator(
        task_id='Sensor-SimpleHttpOperator-985a45e2a',
        http_conn_id='http_connection_1',
        endpoint='/api/v1/resource',
        method='GET'
    )

    sensor_s3keysensor_1b484f59b = S3KeySensor(
        task_id='Sensor-S3KeySensor-1b484f59b',
        bucket_name='my-bucket1',
        bucket_key='my-key1',
        aws_conn_id='aws_connection_1'
    )

    aws_emrcreateclusteroperator_1ac9403d7 = EmrCreateJobFlowOperator(
        task_id='AWS-EMRCreateClusterOperator-1ac9403d7',
        aws_conn_id='aws_connection_1',
        job_flow_overrides="{\\n  \\"master_instance_type\\": \\"m5.xlarge\\",\\n  \\"slave_instance_type\\": \\"m5.xlarge\\",\\n  \\"instance_count\\": 3,\\n  \\"release_label\\": \\"emr-6.10.0\\",\\n  \\"applications\\": [\\n    \\"Spark\\",\\n    \\"Hadoop\\"\\n  ],\\n  \\"log_uri\\": \\"s3://path-to-logs/\\",\\n  \\"keep_cluster_alive\\": False\\n}"
    )

    aws_emrterminatejobflowoperator_a57a4eb87 = EmrTerminateJobFlowOperator(
        task_id='AWS-EmrTerminateJobFlowOperator-a57a4eb87',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='AWS-EMRCreateClusterOperator-1ac9403d7', key='return_value') }}",
        aws_conn_id='aws_default'
    )

        alert_emailoperator_80084a3d6 = EmailOperator(
            task_id='Alert-EmailOperator-80084a3d6',
            to='example@example.com',
            subject='Test Email',
            html_content='<h1>email</h1>'
        )
    # Set task dependencies
    sensor_s3keysensor_1b484f59b >> sensor_simplehttpoperator_985a45e2a
    aws_emrcreateclusteroperator_1ac9403d7 >> sensor_s3keysensor_1b484f59b
    aws_emrterminatejobflowoperator_a57a4eb87 >> aws_emrcreateclusteroperator_1ac9403d7
    alert_emailoperator_80084a3d6 >> aws_emrterminatejobflowoperator_a57a4eb87
