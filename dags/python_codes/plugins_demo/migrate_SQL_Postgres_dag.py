from airflow import DAG
from datetime import datetime, timedelta
from migrate_SQL_Postgres_plugin import MySQLToPostgresHook

from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email import EmailOperator
  
class MySQLToPostgresHook_custom(BaseHook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.info("### custom hook started ###")

    def copy_table(self, mysql_conn_id, postgres_conn_id):
        from airflow.hooks.mysql_hook import MySqlHook
        from airflow.hooks.postgres_hook import PostgresHook

        self.log.info("### fetching records from Postgres table ###")
        postgres_hook = PostgresHook(postgres_conn_id, port=5432)
        postgres_conn = postgres_hook.get_conn()
        postgres_cursor = postgres_conn.cursor()
        
        psql_query = "SELECT * from source"
        data = postgres_cursor.execute(psql_query)
        
        self.log.info('### show records of the data from postgres "source" table ###')
        from pprint import pprint
        pprint(data)

        self.log.info("### Creating and inserting records into MySql table ###")
        mysql_hook = MySqlHook(mysql_conn_id)
        mysql_conn = mysql_hook.get_conn()
        mysql_cursor = mysql_conn.cursor()
        print("list of attribute of mysql_server instance")
        pprint(dir(mysql_conn))
        
        print('# show all tables that exist in mysql')
        x = mysql_cursor.execute("show databases")
        print('show it')
        print(x)        
        
        mysql_cursor.execute('use airflow')
        print('# create a mysql table')
        sql_query0 = "Create table city_table with VALUES(%s, %s, %s);".format(data[0])
        sql_query = "Create table city_table"
        
        mysql_cursor.execute(sql_query)
        print('# insert values from postgres table')
        mysql_conn.execute(f"Insert in city_table values {data[0]}")
        mysql_cursor.commit()
        
        # close cursor
        postgres_conn.close()
        mysql_cursor.close()
        
        # close connection
        postgres_cursor.close()
        mysql_conn.close()
        return True

default_args = dict(
    email_on_failure=True,
    email_on_success=True,  
    email=["amin2prepa@gmail.com"], 
    retries=3,
)

dag = DAG(dag_id='migrate_SQL_Postgres_dag', 
          tags=['plugin'], 
          default_args=default_args,
          schedule_interval=timedelta(1), 
          start_date=datetime(2020, 1, 25), 
          catchup=False)

def trigger_hook():
    MySQLToPostgresHook_custom().copy_table('mysql_conn', 'postgres_conn')
    print("done")

t1 = PythonOperator(
    task_id = 'mysql_to_postgres',
    python_callable = trigger_hook,
    dag = dag
)

t2 = EmailOperator(task_id="Test_email_operator",
                   to=["amin.henteti@ensta-paris.fr",],
                   subject="test Email Operator",
                   html_content="Hi, \nthis is a test mail.\Sincerly",
                   files=["/opt/airflow/plugins/sources.txt",],
                   dag=dag)

t1 >> t2
