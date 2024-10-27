FROM python:3.13-slim

WORKDIR /app

COPY mongodb-configuration/data-sync-app/requirements.txt /app/
COPY mongodb-configuration/data-sync-app/main.py /app/


RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]