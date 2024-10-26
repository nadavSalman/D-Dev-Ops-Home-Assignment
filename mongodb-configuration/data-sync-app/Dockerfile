FROM python:3-slim-buster

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.tx

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]