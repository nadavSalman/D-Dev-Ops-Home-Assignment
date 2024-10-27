FROM python:3.13-slim

WORKDIR /app

COPY mongodb-configuration/data-sync-app/requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]