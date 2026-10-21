from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from pipeline import \
    create_landing_table, \
    ingest_raw, \
    stage_jobs, \
    upsert_jobs, \
    validate_prerequisites
from src.database import validate_staged_jobs

with DAG(
    dag_id="incremental_load",
    start_date=datetime(2026, 10, 1),
    schedule="55 10 * * *",
    catchup=False,
    render_template_as_native_obj=True,
) as dag:

    validate = PythonOperator(
        task_id="validate_prerequisites",
        python_callable=validate_prerequisites,
    )

    create = PythonOperator(
        task_id="create_table",
        python_callable=create_landing_table,
    )

    ingest = PythonOperator(
        task_id="ingest_raw_jobs",
        python_callable=ingest_raw,
        op_kwargs={"landing_table": "{{ ti.xcom_pull('create_table') }}"},
        retries=3,
        retry_delay=timedelta(minutes=5),
        retry_exponential_backoff=True,
    )

    stage = PythonOperator(
        task_id="stage_jobs",
        python_callable = stage_jobs,
        op_kwargs={"landing_table": "{{ ti.xcom_pull('create_table') }}"},
    )

    validate_stage = PythonOperator(
        task_id="validate_staged_jobs",
        python_callable = validate_staged_jobs,
    )

    upsert = PythonOperator(
        task_id="upsert_jobs",
        python_callable = upsert_jobs,
    )

    validate >> create >> ingest >> stage >> validate_stage >> upsert
