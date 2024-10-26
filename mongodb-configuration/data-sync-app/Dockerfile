FROM rtsp/mongosh

WORKDIR /app

COPY . .

# Install necessary dependencies for Python and virtual environment setup
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    python3 -m venv /app/venv

# Activate the virtual environment and install Python dependencies
RUN /app/venv/bin/pip install -r requirements.txt

# Set the entrypoint to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

CMD ["sh"]