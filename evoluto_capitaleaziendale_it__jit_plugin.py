import requests

API_BASE = "https://evoluto.capitaleaziendale.it"

def getFasePrompt(fase_id: str):
    response = requests.get(f"{API_BASE}/get-fase/{fase_id}")
    return response.json()
