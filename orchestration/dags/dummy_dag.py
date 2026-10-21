import pendulum

from airflow.sdk import dag, task


@dag(
    dag_id="dummy_two_task_dag",
    schedule=None,
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
)
def dummy_two_task_dag():

    @task
    def first_task():
        print("First task completed")

    @task
    def second_task():
        print("Second task completed")

    first_task() >> second_task()


dummy_two_task_dag()