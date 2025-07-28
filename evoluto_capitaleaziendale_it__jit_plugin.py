import requests

API_BASE = "https://evoluto.capitaleaziendale.it"

def getFasePrompt(fase_id: str):
    response = requests.get(f"{API_BASE}/get-fase/{fase_id}")
    return response.json()

def verificaChecklistFase(fase_id: str, task_completati: list):
    payload = {
        "fase_id": fase_id,
        "task_completati": task_completati
    }
    response = requests.post(f"{API_BASE}/get-fase-con-verifica", json=payload)
    return response.json()
