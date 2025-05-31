import requests
import json

url = "https://evoluto-app-wa89.onrender.com"

data = {
    "folder_id": "1EKqeDRdoVAk9S9tQyUwXQCsUkKkxnfB7",
    "azienda": {
        "denominazione": "Test Srl"
    }
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.text)
