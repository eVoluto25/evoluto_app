
import requests

def recupera_fase_con_verifica(fase_id: str, task_completati: list[str]):
    url = "https://evoluto.capitaleaziendale.it/get-fase-con-verifica"
    payload = {
        "fase_id": fase_id,
        "task_completati": task_completati
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Errore HTTP: {e.response.status_code} – {e.response.json()}")
        return None
    except Exception as ex:
        print(f"❌ Errore generico: {str(ex)}")
        return None
