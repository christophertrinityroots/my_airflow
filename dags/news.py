from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from config.news_config import news_config
from line import notify
import requests
import json


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 3, 26),
    'email': ['airflow@airflow.com'],
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    "news_to_notify", 
    default_args=default_args,
    schedule_interval=news_config['news_schedule_interval'],
)

dag.catchup = False

#helper functions
def create_country_urls(base_url, api_key):
    def mapper_country_url(country):
        full_news_url = '{0}?country={1}&apiKey={2}'.format(
            base_url,
            country,
            api_key,
        )
        return full_news_url
    return mapper_country_url

def articles_mapper(article):
    allowed_keys = [
        'title',
        'description',
        'url',
        'urlToImage',
    ]
    sub_article = {k:article[k] for k in allowed_keys if k in article} 
    return sub_article

def format_article(article):
    title = article['title']
    description = article['description']
    url = article['url']
    urlToImage = article['urlToImage'] if article['urlToImage'] else ''

    article_struct = "Title: {}\nDescription: {}\nUrl: {}".format(
        title,
        description,
        url,    
    )
    
    article_str = "\n\n{}\n\n".format(article_struct)
    return article_str


# main functions for DAGS
def get_request_urls():
    countries = news_config['news_countries']
    base_url = news_config['news_base_url']
    api_key = news_config['news_api_key']
    request_urls = map(create_country_urls(base_url, api_key), countries)
    return list(request_urls)

def get_news(**context):
    all_articles = []
    urls = context['ti'].xcom_pull(task_ids='get_request_urls')
    for url in urls:
        r = requests.get(url)
        news_dict = json.loads(r.content)
        news_dict = news_dict.get('articles', [])
        all_articles += news_dict
    return all_articles

def clean_articles(**context):
    articles = context['ti'].xcom_pull(task_ids='get_news')
    sub_articles = list(map(articles_mapper, articles))
    return sub_articles

def format_message(**context):
    articles = context['ti'].xcom_pull(task_ids='clean_articles')
    formatted_articles = map(format_article, articles)
    return list(formatted_articles)

def send_line_message(**context):
    welcome_message = str(datetime.now().date())
    notify.lineNotify(welcome_message, news_config['line_notify'])
    articles_list = context['ti'].xcom_pull(task_ids='format_message')
    for article in articles_list:
        notify.lineNotify(article, news_config['line_notify'])
    return True

t0 = PythonOperator(
    task_id="get_request_urls",
    python_callable=get_request_urls,
    dag=dag,
)
t1 = PythonOperator(
    task_id="get_news", 
    python_callable=get_news,
    provide_context=True,
    dag=dag,
)
t2 = PythonOperator(
    task_id="clean_articles", 
    python_callable=clean_articles,
    provide_context=True,
    dag=dag,
)
t3 = PythonOperator(
    task_id="format_message", 
    python_callable=format_message,
    provide_context=True,
    dag=dag,
)
t4 = PythonOperator(
    task_id="send_line_message", 
    python_callable=send_line_message,
    provide_context=True,
    dag=dag,
)

t0 >> t1
t1 >> t2
t2 >> t3
t3 >> t4