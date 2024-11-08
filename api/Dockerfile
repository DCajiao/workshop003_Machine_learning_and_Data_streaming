FROM python:3.9-slim

WORKDIR /api

COPY src /api
COPY requirements.txt /api

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]