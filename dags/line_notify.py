from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import datetime
import requests
import json

def lineNotify(message):
    payload = {'message':message}
    return _lineNotify(payload)

def notifyFile(filename):
    file = {'imageFile':open(filename,'rb')}
    payload = {'message': 'test'}
    return _lineNotify(payload,file)

def notifyPicture(url):
    payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload)

def notifySticker(stickerID,stickerPackageID):
    payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _lineNotify(payload)

def _lineNotify(payload,file=None):
    url = 'https://notify-api.line.me/api/notify'
    token = 'hGZIrYAO51zMiw7VEAt4uONdxgEKWEg8E51LGpb77Px'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data=payload, files=file)

def main_entry():
    lineNotify('Testing Jenkins Auto-Deploy Pipeline. 1, 2, 3')
    return True

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@airflow.com'],
}

dag = DAG(
    "line_notify", 
    default_args=default_args,
    schedule_interval='* * * * *',
    catchup=False,
)

t0 = PythonOperator(
    task_id="line_notify",
    python_callable=main_entry,
    dag=dag,
)