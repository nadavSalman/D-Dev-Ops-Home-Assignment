FROM rtsp/mongosh


# the base image uses a Python environment managed under PEP 668, which restricts system-wide package installations with pip. 
# The solution is to install packages in a virtual environment to avoid breaking the system Python


WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r /app/requirements.txt

ENV PATH="/app/venv/bin:$PATH"

CMD ["sh"]