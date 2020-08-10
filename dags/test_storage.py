from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable #import interface to Variables set in UI
from google.cloud import storage
from google.oauth2 import service_account
import datetime

def list_files(bucket, bucketFolder):
    """List all files in GCP bucket."""
    files = bucket.list_blobs(prefix=bucketFolder)
    return files
    
def get_bucket_cloudstorage(project_id, credentials, bucketName):
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.get_bucket(bucketName)   
    return bucket

def test_storage_connect():
    #get the value of the variable set as cloud_storage_service_account in the UI
    service_account_dict = Variable.get("cloud_storage_service_account", deserialize_json=True)
    #pass dictionary to oauth2 handler
    credentials = service_account.Credentials.from_service_account_info(service_account_dict)
    #get cloud storage bucket using project id, credentials, and name of bucket
    bucket = get_bucket_cloudstorage('roche-277514', credentials, 'trinityroots-roche')
    #list all files in the VM folder
    filelist = list_files(bucket, 'VM')
    print([file.name for file in filelist if '.' in file.name])

def test_variable():
    siteid = Variable.get("siteid", default_var=None)
    table_t = Variable.get("table_t", default_var=None)
    table_t_c = = Variable.get("table_t_c", default_var=None)
    
    for i in siteid:
        print('-----------------------\n test siteid')
        print(i)
    for j in table_t:
        print('-----------------------\n test table_t')
        print(j)
    for k in table_t_c:
        print('-----------------------\n test table_t_c')
        print(k)
    return print ('siteid is',siteid,'\n table_t is',table_t,'\n table_t_c is',table_t_c)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@airflow.com'],
}

dag = DAG(
    "test_variable", 
    default_args=default_args,
    schedule_interval='* * * * *',
    catchup=False,
    max_active_runs=1,
    is_paused_upon_creation=False
)

t0 = PythonOperator(
    task_id="test_variable",
    python_callable=test_variable,
    dag=dag,
)
