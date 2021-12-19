from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2019, 12, 24),
    'catchup': False
}

with DAG("trigger_rules", default_args=default_args, schedule_interval=None,
         catchup=False) as dag:

    t1 = BashOperator(task_id="print_date", bash_command="date")

    t2 = BashOperator(task_id="sleep", bash_command="sleep 5")

    t3 = FileSensor(
        task_id="check_file_exists",
        filepath="/opt/airflow/airflow.db",
        # fs_conn_id="fs_default",
        poke_interval=5,
        timeout=5
    )

    def test_file(*args, **kwargs):
        fs_conn_id, file_path = args
        from logging import log
        from airflow.contrib.hooks.fs_hook import FSHook
        import os
        file_sys_hook = FSHook(fs_conn_id)
        root_path = file_sys_hook.get_path()
        path = os.path.join(root_path, file_path)
        test = os.path.exists(path)
        ti = kwargs['ti']
        ti.xcom_push('test_for_file', test)
        print("### file in {} exists ?\n =>  {}".format(path, test))
        return test

    t33 = PythonOperator(task_id="test_file_exits_by_hook",
                         python_callable=test_file,
                         op_args =("fs_default", '/opt/airflow/airflow-webserver.pid'),
                         retries=5,
                        )

    t4 = BashOperator(
        task_id='final_task',
        bash_command='echo "DONE! file $message"',
        trigger_rule='all_done',# one_success, all_success (done is after success)
                                # 'all_failed' if its all parents are in failed | upstream_failed state.
                                # 'one_failed' fires task when at least one parents failed.
                                #              It does not wait for all parent tasks 
                                #              to get failed.
                                # 'none_failed' not failed or upstream_failed i.e.
                                #               child task in 'success' or 'skipped' status.
                                # 'none_skipped' no parent is in a skipped state.
        env={"message": "{{ ti.xcom_pull(task_ids=['test_file_exits_by_hook'], key='test_for_file') }}"},
        dag=dag
    )

    [t2, t3, t33] >> t4
    t1 >> t2 >> [t3, t33]
