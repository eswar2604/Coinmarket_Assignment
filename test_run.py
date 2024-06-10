import requests
import time

# Base URL for the API
base_url = "http://127.0.0.1:8000/api/taskmanager"

# Payload for the start_scraping endpoint
payload = {
    "coins": ["DUKO", "NOT", "GORILLA"]
}

# Headers for the request
headers = {
    "Content-Type": "application/json"
}

# Send POST request to start_scraping
response = requests.post(f"{base_url}/start_scraping", json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 202:
    data = response.json()
    job_id = data["job_id"]
    print(f"Scraping job started successfully. Job ID: {job_id}")

    # Check the status of the scraping job
    time.sleep(10)  # Wait for a while before checking the status
    status_response = requests.get(f"{base_url}/scraping_status/{job_id}")

    if status_response.status_code == 200:
        print("Scraping status:")
        print(status_response.json())
    else:
        print("Failed to retrieve scraping status")
else:
    print("Failed to start scraping job")
    print(response.json())

