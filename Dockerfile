FROM apache/airflow:2.8.1-python3.11
USER root
COPY requirements.txt requirements.txt
RUN apt update
#    apt install libpq-dev python3-dev build-essential -y
USER airflow
RUN pip install -r requirements.txt