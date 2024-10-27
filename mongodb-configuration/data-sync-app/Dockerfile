FROM python:3.11

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]