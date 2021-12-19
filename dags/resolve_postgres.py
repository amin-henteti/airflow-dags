from cryptography.fernet import Fernet
import os


os.system('echo $FERNET_KEY')
key = Fernet.generate_key()

print(key.decode())
os.environ["FERNET_KEY"] = key.decode()
print("After setting variable")
os.system('echo $FERNET_KEY')
os.system('airflow initdb')