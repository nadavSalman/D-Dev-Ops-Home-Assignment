import os
import sys
from datetime import datetime
import uuid
import requests
import csv
from data_validator.validate import DataValidator

def main():
    # Check if LOCAL_URI environment variable is set
    server_be_endpoint = os.getenv("SERVER_BE_ENDPOINT")
    url = f"{server_be_endpoint}/posts"
    
    if not server_be_endpoint:
        print("Error: SERVER_BE_ENDPOINT environment variable is not configured.")
        sys.exit(1)  


    #(1) Schema Validation
    print('(1) Schema Validation') 
    title = f"Kuku-1-{uuid.uuid4()}"
    print(f"Post Document title  : {title}")
    post_data = {
        "author": "machine",
        "body": "Amendment I\n<p>Congress shall make no law respecting ...",
        "comments": [
            {
                "author": "Santiago Dollins",
                "body": "Lorem ipsum dolor sit amet, consectetur adipisicing...",
                "email": "HvizfYVx@pKvLaagH.com"
            },
            {
                "author": "Jaclyn Morado",
                "body": "Lorem ipsum dolor sit amet, consectetur adipisicing...",
                "email": "WpOUCpdD@hccdxJvT.com"
            }
        ],
        "date": datetime.now().isoformat(),
        "permalink": "aRjNnLZkJkTyspAIoRGe",
        "tags": ["watchmaker", "santa", "xylophone", "math", "handsaw", "dream", "undershirt", "dolphin", "tanker", "action"],
        "title": title
    }

    validator = DataValidator(post_data)
    validator.validate()


    #(2) HTTP POST - Create new post documetn by communicating with the sever-BE app
    print('(2) HTTP POST - Create new post documetn by communicating with the sever-BE app')

    headers = {"Content-Type": "application/json"}

    try:
        post_response = requests.post(post_url, json=post_data, headers=headers)
        post_response.raise_for_status() 

        print("New post document created successfully:", post_response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error during the POST request: {e}")

    #(3) HTTP GRT - Get all posts and save into svc file. For this example to test it, the file will beacssaberl via PV & pvs localstorage . 
    print('(3) HTTP GRT - Get all posts and save into svc file. For this example to test it, the file will beacssaberl via PV & pvs localstorage . ')

    

    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()

        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            header = data[0].keys()

            csv_file_path = '/app/app-posts.csv'
            # csv_file_path = '/home/nadav/dev/Dropit-Dev-Ops-Home-Assignment/mongodb-configuration/data-sync-app/app-posts.csv' # for local test
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                writer.writerows(data)

            print(f"Data saved successfully to {csv_file_path}")
        else:
            print("Unexpected JSON format. Data should be a list of dictionaries.")

    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        
    contents = os.listdir('/app')
    print("Contents of /app:")
    for item in contents:
        print(item)

if __name__ == '__main__':
    main()