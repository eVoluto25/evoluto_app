import requests

# 🔔 1. Funzione per notificare il completamento della fase
def notifica_fase_completata(fase_id: str, utente_id: str = None):
    url = "https://evoluto.capitaleaziendale.it/notifica_fase"
    payload = {
        "fase_id": fase_id,
        "completata": True,
        "utente_id": utente_id  # opzionale, puoi lasciarlo None
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"✅ Notifica inviata per la fase {fase_id}")
        return {"status": "ok"}
    except Exception as ex:
        print(f"❌ Errore notifica fase: {str(ex)}")
        return {"status": "errore", "errore": str(ex)}

# 🔁 2. Recupera fase e verifica checklist, poi notifica completamento
def recupera_fase_con_verifica(fase_id: str, task_completati: list[str], utente_id: str = None):
    url = "https://evoluto.capitaleaziendale.it/get-fase-con-verifica"
    payload = {
        "fase_id": fase_id,
        "task_completati": task_completati
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        fase = response.json()

        # ✅ Invia notifica di completamento
        notifica_fase_completata(fase_id, utente_id=utente_id)

        return fase

    except requests.exceptions.HTTPError as e:
        print(f"❌ Errore HTTP: {e.response.status_code} – {e.response.json()}")
        return None
    except Exception as ex:
        print(f"❌ Errore generico: {str(ex)}")
        return None
