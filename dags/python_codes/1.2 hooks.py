from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'Airflow',
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    'start_date': datetime(2021, 11, 26),
    'catchup': False,
}

dag = DAG('hooks_demo', default_args=default_args, schedule_interval='@daily')

def transfer_function(ds, **kwargs):
    from airflow.hooks.postgres_hook import PostgresHook
    from psycopg2.extras import execute_values
    from pprint import pprint

    query_source = "SELECT * FROM source"
    query_target = "SELECT * FROM target where code like '%N'"
    
    #source hook
    source_hook = PostgresHook(postgres_conn_id='postgres_conn', schema='airflow', port=5444)
    source_conn = source_hook.get_conn()
    source_cursor = source_conn.cursor()

    #target hook
    target_hook = PostgresHook(postgres_conn_id='postgres_conn', schema='airflow', port=5444)
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()

    source_cursor.execute("INSERT INTO source VALUES ('INDIA', 'IN')")
    source_cursor.execute(query_source)
    records = source_cursor.fetchall()
    print('records = ', records)
    if records:
        execute_values(target_cursor, "INSERT INTO target VALUES %s", records)
        target_conn.commit()
        
        # view records in target tables
        target_cursor.execute(query_target)
        new_records = target_cursor.fetchmany(size=113)
        pprint(new_records)

    # close cursor
    source_cursor.close()
    target_cursor.close()
    
    # close connection
    source_conn.close()
    target_conn.close()
    print("Data transferred successfully!")

t1 = PythonOperator(task_id='transfer', python_callable=transfer_function, provide_context=True, dag=dag)


# create table source(city_name varchar (50), city_code varchar (20));
# insert into source (city_name, city_code) values('New York', 'ny'), ('Los Angeles', 'la'), ('Chicago', 'cg'), ('Houston', 'ht');
# create table target as (select * from source) with no data;
# select * from target;
