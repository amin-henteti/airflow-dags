from airflow import DAG
from datetime import datetime, timedelta

from file_count_plugin import FileCountSensor
from airflow.sensors.base import BaseSensorOperator


class FileCountSensor_custom(BaseSensorOperator):
    
    def __init__(self, dir_path, conn_id, *args, **kwargs):
        self.dir_path = dir_path
        self.conn_id = conn_id
        super().__init__(*args, **kwargs)

    def poke(self,context):
        import os
        from airflow.contrib.hooks.fs_hook import FSHook
        hook = FSHook(self.conn_id)
        basepath = hook.get_path()
        full_path = os.path.join(basepath, self.dir_path)
        self.log.info('(basepath = {0}, \nself.dir_path = {1})'.format(basepath, self.dir_path))
        self.log.info('poking location %s', full_path)
        try:
            for root, dirs, files in os.walk(full_path):
                #print(len(files))
                if len(files) >= 5:
                    return True
        except OSError:
            return False
        return False
    
dag = DAG('file_count_dag', tags=['plugin'], 
          schedule_interval=timedelta(1), start_date=datetime(2020, 1, 24), catchup=False)

t1 = FileCountSensor(
    task_id = 'file_count_sensor',
    dir_path = '/usr/local/airflow/plugins',
    conn_id = 'fs_default',
    poke_interval = 5,
    timeout = 100,
    dag = dag
)
