import requests

# FastAPI endpoint URL
url = "http://127.0.0.1:8000/search"

# Test query
query = {"query": "Lab 8"}

# Send request to FastAPI
response = requests.post(url, json=query)

# Display result
if response.status_code == 200:
    print("Search Result:", response.json().get("response"))
else:
    print(f"Error {response.status_code}: {response.text}")
