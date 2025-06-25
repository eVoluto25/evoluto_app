from ast import literal_eval
from datetime import datetime

# --- Mapping equivalenze forma giuridica ---
def verifica_compatibilita_forma_giuridica(forma_giuridica_impresa, tipologia_soggetto_bando):
    mapping_equivalenze = {
        "impresa": ["impresa", "società", "azienda", "micro impresa", "piccola impresa", "media impresa", "PMI"],
        "professionista": ["libero professionista", "professionista", "studio professionale"],
        "cooperativa": ["cooperativa", "società cooperativa"],
        "consorzio": ["consorzio", "rete d’impresa", "ATI"],
        "ente": ["ente", "fondazione", "associazione"],
    }

    tipologia_soggetto_bando = tipologia_soggetto_bando.lower()
    forma_giuridica_impresa = forma_giuridica_impresa.lower()

    for categoria, sinonimi in mapping_equivalenze.items():
        if any(s in forma_giuridica_impresa for s in sinonimi):
            if any(s in tipologia_soggetto_bando for s in sinonimi):
                return True
            else:
                return False
    return True

def classifica_bandi_avanzata(lista_bandi, azienda, tematiche_attive, estensione=False):
    if not lista_bandi:
        return []

    risultati = []
    codice_ateco = azienda["codice_ateco"]
    regione = azienda["regione"].strip().lower()
    dimensione = azienda["dimensione"].strip().lower()
    ebitda = azienda["ebitda"]
    immobilizzazioni = azienda["immobilizzazioni"]
    macro_area = azienda["macro_area"]
    forma_giuridica = azienda.get("forma_giuridica", "").lower()

    for b in lista_bandi:
        if not codice_ateco_compatibile(codice_ateco, b.get("Codici_ATECO", "")):
            continue
        if not regione_compatibile(regione, b.get("Regioni", [])):
            continue
        if not dimensione_compatibile(dimensione, b.get("Dimensioni", "")):
            continue
        if forma_giuridica and not verifica_compatibilita_forma_giuridica(forma_giuridica, b.get("Tipologia_Soggetto", "")):
            continue

        forma_raw = b.get("Forma_agevolazione", "").lower()
        if not estensione and not contiene_fondo_perduto(forma_raw):
            continue
        elif estensione and not contiene_agevolazioni_valide(forma_raw):
            continue

        raw_tematica = b.get("Obiettivo_Finalita", "")
        try:
            tematiche_bando = literal_eval(raw_tematica)
        except:
            tematiche_bando = [t.strip() for t in raw_tematica.split(",") if t.strip()]

        test_score = punteggio_test_bando(tematiche_bando, tematiche_attive)

        punteggi = {
            "obiettivo": punteggio_obiettivo_finalita(b.get("Obiettivo_Finalita", ""), macro_area) * 2,
            "forma": punteggio_forma_agevolazione(b.get("Forma_agevolazione", "")) * 4,
            "scadenza": punteggio_scadenza(b.get("Data_chiusura", "")) * 2,
            "agevolazione_vs_ebitda": punteggio_agevolazione_vs_ebitda(float(b.get("Agevolazione_Concedibile_max", 0) or 0), ebitda) * 3,
            "spesa_compatibile": punteggio_spesa_compatibile(b.get("Spesa_Ammessa_max", 0), immobilizzazioni) * 3,
            "test": punteggio_test_bando(tematiche_bando, tematiche_attive) * 0.3  # Max 15
        }

        totale = round(sum(punteggi.values()), 2)

        if totale >= 70:
            risultati.append({
                **b,
                "punteggi": punteggi,
                "totale": totale,
                "ID_incentivo": b.get("ID_incentivo", None)
            })

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
