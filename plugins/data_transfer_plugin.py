from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator

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

import inspect

class DemoPlugin(AirflowPlugin):
    name = (inspect.stack()[0].filename).split('\\')[-1][:-3] # same as the name of the file
    operators = [DataTransferOperator]
    sensors = []
