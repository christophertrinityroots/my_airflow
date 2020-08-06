FROM puckel/docker-airflow

COPY ./dags /usr/local/airflow/dags
COPY ./requirements/requirements.txt /requirements.txt

EXPOSE 8080 5555 8793
USER airflow