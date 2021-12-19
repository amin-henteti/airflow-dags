from airflow import DAG
from airflow.models import Variable, Connection

from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.models.param import Param

# import module from local directory inside dags folder use relative path
# from python_codes.send_email import sendEmail

default_args = dict(

    #  email_on_failure=True,# this should be False so that we dont get email for failure of any task in our workflow
    #  email_on_retry=True,
    email_on_success=True,  # This is useful when your pipelines have conditional branching,
    #                          # and you want to be notified if a certain path is taken(i.e. certain tasks get run).
    # In order for Airflow to send emails, you need to configure an SMTP server
    email=["amin2prepa@gmail.com"],
    # in your Airflow environment
    # You can do this by filling out the SMTP section of your airflow.cfg
    retries=3,
    # retry_delay=timedelta(seconds=300),
    # # this progressively increases the wait time between retries.
    # # This is useful if you expect that extraneous factors might cause failures periodically.
    # retry_exponential_backoff=True,
    catchup=False
)
# '/' for linux paths because airflow run in linux environment
# import inspect
# dag_name = inspect.stack()[0].filename.split('/')[-1][:-3]
dag = DAG(dag_id='test_template_input_var_conn_email',
          start_date=datetime(2021, 11, 11),
          schedule_interval=None,
          render_template_as_native_obj=True,
          default_args=default_args,
          params={
              'ch': Param('2001-01-01', type="string", format='email', description='give a one word'),
              'n': Param(2, type='integer', minimum=-1, maximum=5, description='please give a number')
              #'other': None # even if this argument is not defined here but 
              # when trigged the templated params contain this key-value pair
          } 
          )


def test_dagRunConfig(ch):
    print(f'the variable in config using dag_run is {ch}')


def test_getVariable(**kwargs):
    var_key = kwargs['var_key']
    x = int(Variable.get(var_key, default_var=1))
    print(
        f'the variable {var_key} defined in Airflow has the value {x} its type is {type(x)}')
    # this should raise an error and its state will be failed
    assert x > 1, f'must increment the value of the variable {var_key}'
    return x


def test_getConnection(**kwargs):
    from airflow import settings
    from airflow.models import Connection
    ti = kwargs['ti']
    ses = settings.Session()
    conns = (ses.query(Connection.host).filter(
        Connection.conn_id.ilike('azure_data_explorer_default')))  # must add () to get uiterable otherwise we have an Object of type Connection is not JSON serializable
    # conns = SELECT connection.conn_id AS connection_conn_id  FROM connection  WHERE lower(connection.conn_id) LIKE lower(?)
    # This is the list of filter operators that can be used:
    # is_null/ is_not_null/ ==, eq/ !=, ne/ >, gt/ <, lt/ >=, ge/ <=, le
    # like/ ilike/ not_ilike/ in_/ not_in/ any/ not_any
    for i, conn in enumerate(conns):
        print(conn)
        # xcom_push(name, var) | xcom_pull(task_ids='', key='')
        # { Key: conn_0,	Value: ['azure_default']}
      #   ti.xcom_push('conn_0', conn[0])
    print("The conns varible = ", conns)  # if len(conns) > 1:
    # return conns
    # print(len(conns))


def func1(*args, **kwargs):
    ti = kwargs['ti']
    from pprint import pprint
    if len(args) < 2:
        args = args[0]
    input_len = len(args)
    print(f"Config parameters are :")
    pprint(args)
    ti.xcom_push('input_len', input_len)
    ti.xcom_push('other', args[-1])
    return 0
    conn_host = ti.xcom_pull(task_ids='test_getConnection', key='conn_0')
    print(f"connection host is {conn_host}")


def func2(*args, **kwargs):
    ti = kwargs['ti']
    x = ti.xcom_pull(task_ids='process_input', key='input_len')
    for _ in range(kwargs['n']):
        print(f"induced args from previous task is {x}")
    try:
        return x+1  # this worked so the pushed value is of type int
    except:
        return x+'1'


def my_callback(context):
    from python_codes.send_email import sendEmail

    dag_run = context.get('dag_run')
    # get_task_instanceS return list of tasks for this dag
    task = dag_run.get_task_instance(task_id='test_getConnection')
    from pprint import pprint
    pprint(dir(task.log.info))
    print(f'task.log.info = {task.log.info}')
    sendEmail(
        objet=f"fail to run the task",
        body_of_email=f"remove len func {task}"
    )

# du -cBM --max-depth=1 2> >(grep -v 'Permission denied') | sort -n 

t = PythonOperator(task_id='test_getVariable',
                   python_callable=test_getVariable,
                   op_kwargs={'var_key': 'x'},
                   dag=dag)


tt = PythonOperator(task_id='test_getConnection',
                    python_callable=test_getConnection,
                    #   email_on_failure=True,  # this specific task will send an email if failed in execution
                    on_failure_callback=my_callback, on_success_callback=my_callback,
                    dag=dag)

t0 = PythonOperator(task_id="test_dag_run",
                    python_callable=test_dagRunConfig,
                    op_kwargs={'ch': "{{ dag_run.conf['ch'] }}"},
                    dag=dag
                    )

t1 = PythonOperator(task_id='process_input',
                    python_callable=func1,
                    op_args=("{{ params['ch'] }}",
                             "{{ params['dag_param'] }}", 
                             "{{ params['other'] }}"),
                    on_success_callback=my_callback,
                    dag=dag)

t2 = PythonOperator(task_id="print",
                    python_callable=func2,
                    op_kwargs={'n': "{{ dag_run.conf['n'] }}", },
                    do_xcom_push=True,  # this will automatically be True if the function return a variable
                    dag=dag)

tt >> t1
tt >> t
t >> t2
[t0, t1] >> t2
