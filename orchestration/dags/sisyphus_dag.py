from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from src.pipeline import ingest_raw_jobs, validate_prerequisites
from src.database import reset_table

with DAG(
    dag_id="sisyphus",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
) as dag:

    validate = PythonOperator(
        task_id="validate_prerequisites",
        python_callable=validate_prerequisites,
    )

    reset = PythonOperator(
        task_id="reset_table",
        python_callable=reset_table,
    )

    ingest_raw = PythonOperator(
        task_id="ingest_raw_jobs",
        python_callable=ingest_raw_jobs,
    )

    validate >> reset >> ingest_raw