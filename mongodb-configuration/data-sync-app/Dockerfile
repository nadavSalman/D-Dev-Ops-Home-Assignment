FROM python:3.11

# Copy main requirements
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy dev requirements 
COPY requirements-dev.txt /app  
RUN pip3 install -r requirements-dev.txt

# Copy test requirements
COPY requirements-test.txt /app
RUN pip3 install -r requirements-test.txt 