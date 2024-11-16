FROM apache/airflow:2.10.2

WORKDIR /app

COPY ./dags/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt