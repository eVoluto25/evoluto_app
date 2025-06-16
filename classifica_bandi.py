
from datetime import datetime

# --- Funzioni di supporto ---

def punteggio_obiettivo_finalita(obiettivo, macro_area):
    priorita = {
        "Espansione, Mercati Esteri e Transizione Ecologica": [
            ("sviluppo impresa", 5),
            ("transizione ecologica", 4),
            ("innovazione", 3),
            ("ricerca", 3),
            ("internazionalizzazione", 2)
        ],
        "Crescita e Sviluppo": [
            ("start up", 5),
            ("sviluppo impresa", 5),
            ("investimenti", 4),
            ("giovani", 3),
            ("femminile", 3)
        ],
        "Crisi o Risanamento Aziendale": [
            ("crisi", 5),
            ("liquidità", 4),
            ("inclusione sociale", 3),
            ("riconversione", 3),
            ("reinserimento", 2)
        ]
    }
    chiavi = priorita.get(macro_area, [])
    obiettivo = obiettivo.lower()
    for parola, punteggio in chiavi:
        if parola in obiettivo:
            return punteggio
    return 1

def punteggio_forma_agevolazione(forma):
    forma = forma.lower()
    if "fondo perduto" in forma:
        return 5
    elif "agevolazione fiscale" in forma:
        return 4
    elif "prestito" in forma or "anticipo" in forma:
        return 3
    elif "garanzia" in forma:
        return 2
    else:
        return 1

def punteggio_scadenza(data_str):
    try:
        data = datetime.fromisoformat(data_str.split("T")[0])
        giorni = (data - datetime.today()).days
        if giorni < 60:
            return 0
        elif giorni <= 90:
            return 5
        elif giorni <= 180:
            return 3
        else:
            return 1
    except:
        return 0

def punteggio_agevolazione_vs_ebitda(agevolazione, ebitda):
    if agevolazione <= ebitda * 0.3:
        return 5
    elif agevolazione <= ebitda:
        return 3
    else:
        return 1

def punteggio_spesa_compatibile(spesa, immobilizzazioni):
    if spesa <= immobilizzazioni * 0.3:
        return 5
    elif spesa <= immobilizzazioni:
        return 3
    else:
        return 1

def codice_ateco_compatibile(codice_azienda, codici_bando):
    return "tutti" in codici_bando.lower() or any(codice.strip() in codici_bando for codice in codice_azienda)

def regione_compatibile(regione_azienda, regioni_bando):
    return regione_azienda in regioni_bando

def dimensione_compatibile(dim_azienda, dim_bando):
    return "tutte" in dim_bando.lower() or dim_azienda in dim_bando

# --- Funzione principale ---

def classifica_bandi_avanzata(lista_bandi, azienda):
    risultati = []
    codice_ateco = [azienda["codice_ateco"]]
    regione = azienda["regione"]
    dimensione = azienda["dimensione"]
    ebitda = azienda["ebitda"]
    immobilizzazioni = azienda["immobilizzazioni"]
    macro_area = azienda["macro_area"]

    for b in lista_bandi:
        if not codice_ateco_compatibile(codice_ateco, b.get("Codici_ATECO", "")):
            continue
        if not regione_compatibile(regione, b.get("Regioni", [])):
            continue
        if not dimensione_compatibile(dimensione, b.get("Dimensioni", "")):
            continue

        punteggi = {
            "obiettivo": punteggio_obiettivo_finalita(b.get("Obiettivo_Finalita", ""), macro_area),
            "forma": punteggio_forma_agevolazione(b.get("Forma_agevolazione", "")),
            "scadenza": punteggio_scadenza(b.get("Data_chiusura", "")),
            "agevolazione_vs_ebitda" = punteggio_agevolazione_vs_ebitda(float(b.get("Agevolazione_Concedibile_max", 0) or 0), ebitda)
            "spesa_compatibile": punteggio_spesa_compatibile(b.get("Spesa_Ammessa_max", 0), immobilizzazioni)
        }

        totale = sum(punteggi.values())

        risultati.append({
            **b,
            "punteggi": punteggi,
            "totale": totale
        })

    # Ordinamento ibrido: in caso di parità si applicano criteri secondari
    risultati.sort(
        key=lambda x: (
            x["totale"],
            x["punteggi"]["obiettivo"],
            x["punteggi"]["scadenza"],
            x["punteggi"]["forma"],
            x.get("Agevolazione_Concedibile_max", 0),
            x.get("Spesa_Ammessa_max", 0)
        ),
        reverse=True
    )

    return risultati[:3]
