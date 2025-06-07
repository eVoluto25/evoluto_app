from datetime import datetime
from simulatore_impatto import simula_beneficio
from motivazione_bando import genera_motivazione

def calcola_match_bando(bando: dict, macroarea: str) -> dict:
    finalita = bando.get("obiettivo_finalita", "").lower()

    parole_chiave = {
        "Crisi": ["crisi d’impresa", "sostegno liquidità", "inclusione sociale"],
        "Crescita": ["start up", "sviluppo d’impresa", "sostegno investimenti", "imprenditoria giovanile", "imprenditoria femminile"],
        "Espansione": ["internazionalizzazione", "sviluppo d’impresa", "transizione ecologica", "innovazione", "ricerca"]
    }.get(macroarea, [])

    # ✅ FILTRO sulla data di chiusura (solo se non ci sono note positive)
    data_chiusura_str = bando.get("Data_chiusura", "")
    if data_chiusura_str:
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

def trova_bandi_compatibili(azienda_id: str, azienda: dict) -> None:
    risultati = []
    for bando in bandi:
        # Filtro di sostenibilità economica: esclude bandi non sostenibili per l'azienda
        try:
            spesa_min = float(bando.get("spesa_ammessa_min", 0))
            fatturato = float(azienda.get("fatturato", 1))
            liquidita = float(azienda.get("liquidita", 0))
            utile = float(azienda.get("utile_netto", 0))
            
            # Calcolo soglia massima sostenibile (20% del fatturato)
            soglia_massima = fatturato * 0.20
            capacita_finanziaria = liquidita + utile

            # Se non è in crisi e non ha forza per sostenere la spesa minima, scarta
            if "crisi" not in macroarea and spesa_min > 0:
            if spesa_min > soglia_massima and capacita_finanziaria < spesa_min:
                continue  # Salta questo bando
        except Exception as e:
            print(f"[Filtro Spesa Ammessa] Errore: {e}")
     
        match = calcola_match_bando(bando, macroarea)
        if match:
            # ⬇️ Simulazione dell'impatto economico
            beneficio = simula_beneficio(bando, azienda)
            match["commento_impatto"] = beneficio.get("commento", "")
            match["roi_stimato"] = beneficio.get("roi_stimato", 0)
            
            risultati.append(match)

        # Filtro per punteggio minimo e selezione Top 5
        bandi_filtrati = [r for r in risultati if r.get("punteggio_compatibilità", 0) >= 80]
        bandi_ordinati = sorted(bandi_filtrati, key=lambda x: x.get("punteggio_compatibilità", 0), reverse=True)
        top5 = bandi_ordinati[:5]

        # Sovrascrive i risultati con i top5 selezionati
        risultati = top5
        return risultati

        # Filtro Top 5 bandi con punteggio >= 80 e ordinamento decrescente
        top5 = sorted(
            [b for b in risultati_match if b.get('punteggio', 0) >= 80],
            key=lambda x: x.get('beneficio_stimato', 0),
            reverse=True
        )[:5]

        # Serializza solo i dati rilevanti
        top5_serializzati = [
            {
               "id": b.get("id"),
               "titolo": b.get("titolo"),
               "punteggio": b.get("punteggio"),
               "beneficio_stimato": b.get("beneficio_stimato"),
               "forma_agevolazione": b.get("forma_agevolazione"),
               "data_chiusura": b.get("data_chiusura"),
               "motivazione": genera_motivazione(b)
            } for b in top5
        ]

        # Aggiorna la tabella Supabase
        supabase_client.table("verifica_aziendale").update({
            "top5_bandi": top5_serializzati
        }).eq("id", id_verifica).execute()

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
