from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.sensors.base import BaseSensorOperator
import logging as log
from airflow.contrib.hooks.fs_hook import FSHook
import os
import stat
# for custom hooks
from airflow.hooks.base_hook import BaseHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.postgres_hook import PostgresHook


class DataTransferOperator(BaseOperator):

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


class FileCountSensor(BaseSensorOperator):

    def __init__(self, dir_path, conn_id, *args, **kwargs):
        self.dir_path = dir_path
        self.conn_id = conn_id
        super().__init__(*args, **kwargs)

    def poke(self, context):
        import os
        hook = FSHook(self.conn_id)
        basepath = hook.get_path()
        full_path = os.path.join(basepath, self.dir_path)
        self.log.info('(basepath = {0}, \nself.dir_path = {1})'.format(
            basepath, self.dir_path))
        self.log.info('poking location %s', full_path)
        try:
            for root, dirs, files in os.walk(full_path):
                # print(len(files))
                if len(files) >= 5:
                    return True
        except OSError:
            return False
        return False


class MySQLToPostgresHook(BaseHook):
    def __init__(self):
        self.log.info("##custom hook started##")

    def copy_table(self, mysql_conn_id, postgres_conn_id):

        self.log.info("### fetching records from MySQL table ###")
        mysqlserver = MySqlHook(mysql_conn_id)
        sql_query = "SELECT * from city_table"
        data = mysqlserver.get_records(sql_query)

        self.log.info("### inserting records into Postgres table ###")
        postgresserver = PostgresHook(postgres_conn_id)
        postgres_query = "INSERT INTO city_table VALUES(%s, %s, %s);"
        postgresserver.insert_rows(table='city_table', rows=data)

        return True


class DemoPlugin(AirflowPlugin):
    name = "demo_plugin"
    operators = [DataTransferOperator]
    sensors = [FileCountSensor]
    hooks = [MySQLToPostgresHook]
