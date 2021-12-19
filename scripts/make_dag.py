import os
import subprocess
import sys
import json
import re
import dataclasses
# end first line with \ to avoid the empty line!

template = """\
from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'amin',
    'depends_on_past': False,
    'email': ['aminhenteti@soge.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2022, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'tutorial', # DAG_id
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
"""

filename = sys.argv[1] if len(sys.argv) > 1 else "new_dag.py"
if not(filename.endswith('.py')):
    filename += '.py'
assert os.path.exists(
    filename), "the file already exist, please use a different file name"

with open(filename, 'w') as f:
    f.write(template)


@task
def get_data():
    url = "https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/pipeline_example.csv"

    response = requests.request("GET", url)

    with open("/usr/local/airflow/dags/files/employees.csv", "w") as file:
        for row in response.text.split("\n"):
            file.write(row)

    postgres_hook = PostgresHook(postgres_conn_id="LOCAL")
    conn = postgres_hook.get_conn()
    cur = conn.cursor()
    with open("/usr/local/airflow/dags/files/employees.csv", "r") as file:
        cur.copy_from(
            f,
            "Employees_temp",
            columns=[
                "Serial Number",
                "Company Name",
                "Employee Markme",
                "Description",
                "Leave",
            ],
            sep=",",
        )
    conn.commit()
