FROM python:3-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]