# Use an official MongoDB image as a base
FROM rtsp/mongosh

# Set the working directory
WORKDIR /app

# Copy your Python application files into the container
COPY . .

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install necessary Python packages
# RUN pip3 install -r requirements.txt

# Run MongoDB and your Python script
CMD ["sh"]
