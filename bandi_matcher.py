from datetime import datetime

def calcola_match_bando(bando: dict, macroarea: str) -> dict:
    finalita = bando.get("obiettivo_finalita", "").lower()

    parole_chiave = {
        "Crisi": ["crisi d’impresa", "sostegno liquidità", "inclusione sociale"],
        "Crescita": ["start up", "sviluppo d’impresa", "sostegno investimenti", "imprenditoria giovanile", "imprenditoria femminile"],
        "Espansione": ["internazionalizzazione", "sviluppo d’impresa", "transizione ecologica", "innovazione", "ricerca"]
    }.get(macroarea, [])

    # ✅ FILTRO sulla data di chiusura (solo se non ci sono note positive)
    data_chiusura_str = bando.get("Data_chiusura", "")
    note = bando.get("Note_di_apertura_chiusura", "").lower()
    if "a sportello" not in note and "fino ad esaurimento" not in note and "prorogato" not in note:
        if data_chiusura_str:
            try:
                data_chiusura = datetime.strptime(data_chiusura_str, "%Y-%m-%dT%H:%M:%S")
                if data_chiusura < datetime.today():
                   return None  # Bando chiuso
           except ValueError:
               pass  # formato errato, ignora filtro

    # ✅ Filtro su Codici ATECO
    codici = bando.get("Codici_ATECO", "")
    if "tutti i settori economici ammissibili" not in codici.lower():
        if codice_ateco_azienda not in codici.replace(" ", "").split(";"):
            return None

    # ✅ Filtro su Settore Attività
    settore_bando = bando.get("Settore_Attivita", "").lower()
    if settore_bando and settore_attivita_azienda.lower() not in settore_bando:
        return None

    # ✅ Filtro su Regione
    regioni_bando = bando.get("Regioni", "").lower()
    if regioni_bando:
        regione_azienda = regione_azienda.lower()
        if regione_azienda not in regioni_bando:
            return None

    # ✅ Filtro su Spesa Ammessa
    try:
        spesa_min = float(bando.get("Spesa_ammessa_min", "0"))
        soglia = 0.2 * fatturato_azienda
        if spesa_min > soglia and (spesa_min > liquidita_azienda or spesa_min > utile_netto_azienda):
            return None
    except ValueError:
        pass
            
    # ✅ Filtro su parole chiave della macroarea
    if any(kw in finalita for kw in parole_chiave):
        return {
            "Titolo": bando.get("titolo", ""),
            "Link_istituzionale": bando.get("link", ""),
            "Ambito_territoriale": bando.get("ambito_territoriale", "")
        }

    return None

def trova_bandi_compatibili(bandi: list, macroarea: str) -> list:
    risultati = []
    for bando in bandi:
        match = calcola_match_bando(bando, macroarea)
        if match:
            risultati.append(match)
    return risultati

def aggiorna_tabella_verifica(supabase_client, id_verifica: str, risultati_match: list):
    if not risultati_match:
        return

    # 1. Cancella righe precedenti
    supabase_client.table("verifica_aziendale").delete().eq("id_verifica", id_verifica).execute()

    # 2. Inserisce tutte le righe compatibili con lo stesso id_verifica
    righe_da_inserire = []
    for match in risultati_match:
        match["id_verifica"] = id_verifica
        righe_da_inserire.append(match)

    supabase_client.table("verifica_aziendale").insert(righe_da_inserire).execute()
