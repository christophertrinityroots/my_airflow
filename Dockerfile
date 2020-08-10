FROM puckel/docker-airflow

COPY ./dags /usr/local/airflow/dags
COPY ./requirements/requirements.txt /requirements.txt
USER root

# add cloud sdk 
# RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y --force-yes
RUN sudo apt-get install libpq-dev
RUN pip install --upgrade pip
RUN pip install petl \
    && pip install xlrd \
    && pip install openpyxl \
    && pip install mysql-connector==2.2.9 \
    && pip install psycopg2 \
    && pip install sqlalchemy \
    && pip install numpy \
    && pip install pandas \
    && pip install google-cloud-storage \
    && pip install configparser \
    && pip install urllib3
    
EXPOSE 8080 5555 8793
USER airflow
