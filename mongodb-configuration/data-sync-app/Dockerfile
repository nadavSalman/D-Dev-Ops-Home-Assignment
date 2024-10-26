FROM python:3

#set envionment variables
ENV PYTHONUNBUFFERED 1

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip


#set work directory early so remaining paths can be relative
WORKDIR /app

COPY requirements.txt .


#install dependencies
RUN pip install -r requirements.txt

# copy code itself from context to image
COPY . .

CMD ["python", "main.py"]