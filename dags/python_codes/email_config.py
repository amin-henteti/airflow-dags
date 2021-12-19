# Either paste this inside your airflow.cfg:
"""
[smtp]
# If you want airflow to send emails on retries, failure, and you want to use
# the airflow.utils.email.send_email_smtp function, you have to configure an
# smtp server here
smtp_host = your-smtp-host.com
smtp_starttls = True
smtp_ssl = False
# Uncomment and set the user/pass settings if you want to use SMTP AUTH
# smtp_user =
# smtp_password =
smtp_port = 587
smtp_mail_from = noreply@astronomer.io
"""
# Otherwise set these values using environment variables.
# In this case, all parameters are preceded by AIRFLOW__SMTP__,
# consistent with Airflow environment variable naming convention.
# Example, smtp_host can be specified by setting the AIRFLOW__SMTP__SMTP_HOST variable

from pprint import pprint
import os
import sys
options = dict(smtp_host="your-smtp-host.com",
               smtp_starttls = "True", smtp_ssl = "False",
               smtp_user = "", smtp_password = "", 
               smtp_port = "587", smtp_mail_from = "noreply@astronomer.io")
import subprocess
os.environ['afid'] = "b2"
subprocess.call(['printenv', 'afid'])
sys.exit()
# The following method dosent work 
# commands = [f'export AIRFLOW__SMTP__{op.upper()}={val}' for op,val in options.items() if val] # val = "" is evaluated as False
# pprint(commands)
# for cmd in commands:
#     os.system(cmd)

# envirnment variable values must be of type string
myenv = os.environ.copy()
for op,val in options.items():
    env_var = f"AIRFLOW__SMTP__{op.upper()}"
    print(env_var)
    myenv[env_var] = val
cmd = "export AIRFLOW__SMTP__SMTP_PORT=587"