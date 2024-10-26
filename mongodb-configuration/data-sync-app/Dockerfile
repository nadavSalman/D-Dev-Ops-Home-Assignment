FROM python:3-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.tx

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]