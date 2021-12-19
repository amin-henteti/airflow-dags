import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.email import EmailOperator


args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

def push_function(**kwargs):
    pushed_value= 16
    ti = kwargs['ti']
    ti.xcom_push(key="pushed_value", value=pushed_value)

def branch_function(**kwargs):
    ti = kwargs['ti']
    pulled_value = ti.xcom_pull(key='pushed_value', task_ids='push_task')
    if pulled_value % 3 == 0:
        return '0_mod_3_task'
    elif pulled_value % 3 == 1 and pulled_value % 5 == 1:
        return ['1_mod_3_task', '1_mod_5_task']
    else:
        return ['2_mod_3_task', '0_mod_3_task']

def send_mail_task(**kwargs):
    from python_codes.send_email import sendEmail
    ti = kwargs['ti']
    sendEmail(
        objet=f"branch task",
        body_of_email="The attributes of the task are like log are :\n{}".format('\n'.join(dir(ti)))
    )
    
with DAG(dag_id='branching', default_args=args, schedule_interval="@daily",) as dag:

    push_task = PythonOperator(task_id='push_task', python_callable=push_function, 
    provide_context=True)

    branch_task = BranchPythonOperator(task_id='branch_task', python_callable=branch_function, provide_context=True)

    zero_mod_3_task = BashOperator(task_id='0_mod_3_task', bash_command='echo "The given value : \n$value is divisible by 3"',
                                   env={'value' : '{{ti.xcom_pull(key="pushed_value", task_ids="push_task")}}'})
    one_mod_3_task = BashOperator(task_id='1_mod_3_task', bash_command='echo "The given value : \n$value = 1 mod [3]"',
                                   env={'value' : '{{ti.xcom_pull(key="pushed_value", task_ids="push_task")}}'})
    two_mod_3_task = BashOperator(task_id='2_mod_3_task', bash_command='echo "The given value : \n$value = 2 mod [3]"',
                                   env={'value' : '{{ti.xcom_pull(key="pushed_value", task_ids="push_task")}}'})
    one_mod_5_task = BashOperator(task_id='1_mod_5_task', bash_command='echo "The given value : \n$value = 2 mod [5]"',
                                   env={'value' : '{{ti.xcom_pull(key="pushed_value", task_ids="push_task")}}'})
    send_email = PythonOperator(task_id="send_email_task",
                   python_callable=send_mail_task,
                   trigger_rule = 'one_success',
                   dag=dag)
              
    push_task >> branch_task >>[zero_mod_3_task, one_mod_3_task, two_mod_3_task, one_mod_5_task] >> send_email
