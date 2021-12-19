from os import system
import sys
# pay attension to the log folder if it is mounted then this can cause problems
# if so rename the folderS where we write logs in airflow.cfg

path_to_dcc = '/c/Users/Public/Airflow/' # path to docker compose 
commands = [   
    # f'docker cd {path_to_dcc}'
    # 'pip install plyvel',
    # 'airflow users create -r Admin -u henteti -p xx -f amin -l henteti -e aminhenteti21@gmail.com',
    # 'airflow db init',
    
    'ls /opt/airflow/',
    'rm /opt/airflow/*-*',
    'ls /opt/airflow/',
    'airflow scheduler -D',
    'ls /opt/airflow/',
    'airflow webserver -D',
    'ls /opt/airflow/',
]
for cmd in commands:
    print(f"executing {cmd}")
    x = system(cmd)
    if x != 0:
        print(f"status code = {x}")
        break
    print(55*'_')
    
    