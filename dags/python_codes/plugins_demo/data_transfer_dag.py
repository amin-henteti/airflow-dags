from airflow.models.param import Param
from airflow import DAG
from datetime import datetime, timedelta

from data_transfer_plugin import DataTransferOperator
from airflow.models import BaseOperator
# from airflow.utils.decorators import apply_defaults


class DataTransferOperator_custom(BaseOperator):
    template_fields = ['delete_list']
    def __init__(self, source_file_path, dest_file_path, delete_list, *args, **kwargs):

        self.source_file_path = source_file_path
        self.dest_file_path = dest_file_path
        self.delete_list = delete_list
        super().__init__(*args, **kwargs)

    def execute(self, context):
        import logging as log

        SourceFile = self.source_file_path
        DestinationFile = self.dest_file_path
        DeleteList = self.delete_list

        self.log.info("### custom operator execution starts ###")
        self.log.info('source_file_path: %s', SourceFile)
        self.log.info('dest_file_path: %s', DestinationFile)
        self.log.info('delete_list: %s', DeleteList)

        fin = open(SourceFile)
        fout = open(DestinationFile, "a")

        # file processing
        for line in fin:
            self.log.info('### reading line: %s', line)
            for word in DeleteList:
                self.log.info('### matching string: %s', word)
                line = line.replace(word, "")

            self.log.info('### output line is: %s', line)
            fout.write(line)

        fin.close()
        fout.close()

dag = DAG('data_transfer_dag',  tags=['plugin'],
          params={
    "list of words to delete": Param(["is", ','], list),
    "action": "delete",
},
    render_template_as_native_obj=True, # because we are using list
    schedule_interval=timedelta(1), start_date=datetime(2020, 1, 24), catchup=False)


t1 = DataTransferOperator(
    task_id='data_transfer_task',
    source_file_path='/opt/airflow/plugins/source.txt',
    dest_file_path='/opt/airflow/plugins/destination.txt',
    # ['Airflow', 'is'],
    delete_list="{{ params['list of words to delete'] }}",
    dag=dag
)
