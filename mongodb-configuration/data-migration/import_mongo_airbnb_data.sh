#!/bin/bash

# ./script.sh *<uri>  #


MONGO_URI=$1

# Download the JSON data from the provided URL
URL="https://raw.githubusercontent.com/neelabalan/mongodb-sample-dataset/refs/heads/main/sample_airbnb/listingsAndReviews.json"
DATA_FILE="listingsAndReviews.json"

echo "Downloading data from $URL..."
curl -o $DATA_FILE $URL

# Check if the file was downloaded successfully
if [ -f "$DATA_FILE" ]; then
    echo "File downloaded successfully."
    
    # Import into MongoDB under sample_airbnb database and listingsAndReviews collection
    mongoimport --drop --uri "$MONGO_URI" --db "sample_airbnb" --collection "listingsAndReviews" --file "$DATA_FILE" $auth
else
    echo "Failed to download the file."
fi
