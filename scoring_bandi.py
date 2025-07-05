import datetime

def calcola_scoring_bandi(bandi: list, azienda: dict, valutazione_evoluto: int = 80) -> list:
    """
    Applica lo scoring finale ai bandi pre-filtrati.
    
    Args:
        bandi: lista di dizionari con i dati dei bandi.
        azienda: dict con info aziendali (es. regione, ebitda, utile netto, fatturato).
        valutazione_evoluto: valutazione integrativa (0-100).
    
    Returns:
        Lista di bandi con punteggi e classificazione.
    """
    risultati = []
    oggi = datetime.date.today()
    for b in bandi:
        punteggi = {}

        # 1. Compatibilità Territorio
        if azienda["regione"] in [r.lower() for r in [s.lower() for s in b.get("Obiettivo Bando", [])]]:
            punteggi["Compatibilità Territorio"] = 5
        else:
            punteggi["Compatibilità Territorio"] = 2

        # 2. Percentuale Spesa
        perc = b.get("Percentuale Spesa", "Non definita").replace("%", "").strip()
        if perc == "Non definita":
            punteggi["Percentuale Spesa"] = 10
        else:
            perc_float = float(perc)
            if perc_float >= 70:
                punteggi["Percentuale Spesa"] = 15
            else:
                punteggi["Percentuale Spesa"] = 10

        # 3. Cofinanziamento
        cofin_percentuale = (azienda["ebitda"] + azienda["utile_netto"]) / azienda["fatturato"] * 100 if azienda["fatturato"] > 0 else 0
        if cofin_percentuale >= 10:
            punteggi["Cofinanziamento"] = 20
        elif 5 <= cofin_percentuale < 10:
            punteggi["Cofinanziamento"] = 15
        else:
            punteggi["Cofinanziamento"] = 10

        # 4. Prossimità Scadenza
        data_str = b.get("Data Scadenza", "")
        giorni = 180
        if "fino ad esaurimento" in data_str.lower():
            giorni = 180
        else:
            try:
                data_bando = datetime.datetime.strptime(data_str, "%d/%m/%Y").date()
                giorni = (data_bando - oggi).days
            except Exception:
                giorni = 180
        if giorni >= 180:
            punteggi["Prossimità Scadenza"] = 5
        elif 90 <= giorni < 180:
            punteggi["Prossimità Scadenza"] = 10
        else:
            punteggi["Prossimità Scadenza"] = 15

        # 5. Solidità Aziendale
        punteggi["Solidità Aziendale"] = 10

        # 6. Allineamento Obiettivo
        if b.get("Prioritario SI/NO", "NO") == "SI":
            punteggi["Allineamento Obiettivo"] = 10
        else:
            punteggi["Allineamento Obiettivo"] = 0

        # 7. Tipo Agevolazione
        tipo = b.get("Tipo Agevolazione", "").lower()
        if "fondo perduto" in tipo:
            punteggi["Tipo Agevolazione"] = 10
        elif "finanziamento" in tipo:
            punteggi["Tipo Agevolazione"] = 5
        else:
            punteggi["Tipo Agevolazione"] = 3

        # 8. Compatibilità ATECO
        punteggi["Compatibilità ATECO"] = 5

        # Totale punti oggettivi
        totale_punti = sum(punteggi.values())
        prob_approvazione = (totale_punti / 85) * 100

        # Punteggio finale ponderato
        punteggio_finale = ((prob_approvazione) * 0.7) + (valutazione_evoluto * 0.3)

        # Classificazione qualitativa
        if punteggio_finale >= 90:
            classificazione = "🔵 ECCELLENTE"
        elif punteggio_finale >= 75:
            classificazione = "🟢 BUONO"
        elif punteggio_finale >= 60:
            classificazione = "🟡 ADEGUATO"
        elif punteggio_finale >= 40:
            classificazione = "🟠 BASSA COERENZA"
        else:
            classificazione = "🔴 NON RACCOMANDATO"

        # Filtro qualità minima
        if prob_approvazione < 50 or punteggio_finale < 60:
            continue

        # Aggiorna il bando con i nuovi dati
        bando_completo = b.copy()
        bando_completo.update({
            "Dettaglio Criteri": punteggi,
            "Totale punti oggettivi": totale_punti,
            "Probabilità di approvazione (%)": round(prob_approvazione, 1),
            "Punteggio finale": round(punteggio_finale, 1),
            "Classificazione": classificazione
        })

        risultati.append(bando_completo)

    if not risultati:
        return [{"messaggio": "Il sistema eVoluto ha completato l’analisi ma non ha individuato bandi con un livello minimo di compatibilità e probabilità di approvazione. Si suggerisce di aggiornare i dati aziendali o attendere nuovi incentivi."}]
    return risultati
