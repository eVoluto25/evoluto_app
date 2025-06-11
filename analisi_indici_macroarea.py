import logging

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def safe_divide(numerator, denominator):
    try:
        result = numerator / denominator if denominator != 0 else "ND"
        return result
    except Exception as e:
        logging.warning(f"Errore nel calcolo: {e}")
        return "ND"

def calcola_indici(dati):
    logging.info("Inizio calcolo dei 25 indici finanziari.")
    try:
        indici = {
            "ROE": safe_divide(dati.get("Risultato Netto", 0), dati.get("Patrimonio Netto", 0)),
            "ROI": safe_divide(dati.get("Risultato Operativo", 0), dati.get("Capitale Investito Netto Operativo", 0)),
            "ROS": safe_divide(dati.get("Risultato Operativo", 0), dati.get("Vendite", 0)),
            "ROT": safe_divide(dati.get("Vendite", 0), dati.get("Capitale Investito Netto Operativo", 0)),
            "ROIC": safe_divide(dati.get("NOPAT", 0), dati.get("Media Capitale Investito Netto Operativo", 0)),

            "Copertura Immobilizzazioni": safe_divide(dati.get("Patrimonio Netto", 0) + dati.get("Passività a lungo", 0), dati.get("Attivo Immobilizzato", 0)),
            "Indipendenza Finanziaria": safe_divide(dati.get("Patrimonio Netto", 0), dati.get("Totale Attivo", 0)),
            "Leverage": safe_divide(dati.get("Totale Attivo", 0), dati.get("Patrimonio Netto", 0)),
            "PFN/PN": safe_divide(dati.get("Posizione Finanziaria Netta", 0), dati.get("Patrimonio Netto", 0)),

            "Current Ratio": safe_divide(dati.get("Attività a breve", 0), dati.get("Passività a breve", 0)),
            "Quick Ratio": safe_divide(dati.get("Attività a breve", 0) - dati.get("Rimanenze", 0), dati.get("Passività a breve", 0)),
            "Margine di Tesoreria": safe_divide(dati.get("Attività liquide", 0), dati.get("Passività correnti", 0)),
            "Margine di Struttura": safe_divide(dati.get("Patrimonio Netto", 0), dati.get("Totale Attivo", 0)),
            "Capitale Circolante Netto": dati.get("Attività a breve", 0) - dati.get("Passività a breve", 0),

            "EBIT/OF": safe_divide(dati.get("Risultato Operativo", 0), dati.get("Oneri Finanziari", 0)),
            "MOL/PFN": safe_divide(dati.get("Margine Operativo Lordo", 0), dati.get("Posizione Finanziaria Netta", 0)),
            "Flusso di Cassa / OF": safe_divide(dati.get("Flusso di Cassa operativo", 0), dati.get("Oneri Finanziari", 0)),
            "PFN/MOL": safe_divide(dati.get("Posizione Finanziaria Netta", 0), dati.get("Margine Operativo Lordo", 0)),
            "PFN/Ricavi": safe_divide(dati.get("Posizione Finanziaria Netta", 0), dati.get("Ricavi", 0)),

            "Cash Wallet Risk Index": dati.get("Cash Wallet Risk Index", "ND"),
            "Collateral Distortion Index": dati.get("Collateral Distortion Index", "ND"),
            "Sconfinamento Medio": dati.get("Sconfinamento Medio", "ND"),
            "Tensione Finanziaria": dati.get("Tensione Finanziaria", "ND"),
            "Cash Wallet Management Index": dati.get("Cash Wallet Management Index", "ND"),
            "Duration": dati.get("Duration", "ND")
        }

        logging.info("Indici calcolati con successo.")
        return indici
    except Exception as e:
        logging.error(f"Errore durante il calcolo degli indici: {e}")
        return {}

def assegna_macro_area(indici):
    logging.info("Inizio assegnazione della macro area.")
    try:
        punti_crisi = 0
        punti_crescita = 0
        punti_espansione = 0

        #  Crisi
        if isinstance(indici["Current Ratio"], (int, float)) and indici["Current Ratio"] <= 1:
            punti_crisi += 1
        if isinstance(indici["PFN/PN"], (int, float)) and 0.5 <= indici["PFN/PN"] <= 2:
            punti_crisi += 1
        if isinstance(indici["EBIT/OF"], (int, float)) and indici["EBIT/OF"] < 1:
            punti_crisi += 1
        if isinstance(indici["MOL/PFN"], (int, float)) and indici["MOL/PFN"] > 0:
            punti_crisi += 1
        if isinstance(indici["ROE"], (int, float)) and indici["ROE"] > 0:
            punti_crisi += 1

        #  Crescita
        if isinstance(indici["Capitale Circolante Netto"], (int, float)) and indici["Capitale Circolante Netto"] > 0:
            punti_crescita += 1
        if isinstance(indici["Indipendenza Finanziaria"], (int, float)) and indici["Indipendenza Finanziaria"] > 0.2:
            punti_crescita += 1
        if isinstance(indici["Copertura Immobilizzazioni"], (int, float)) and indici["Copertura Immobilizzazioni"] > 1:
            punti_crescita += 1

        #  Espansione
        if isinstance(indici["ROS"], (int, float)) and indici["ROS"] > 0.05:
            punti_espansione += 1
        if isinstance(indici["MOL/PFN"], (int, float)) and indici["MOL/PFN"] > 0.1:
            punti_espansione += 1
        if isinstance(indici["ROIC"], (int, float)) and indici["ROIC"] > 0.05:
            punti_espansione += 1

        logging.info(f"Punteggi: Crisi={punti_crisi}, Crescita={punti_crescita}, Espansione={punti_espansione}")

        if punti_espansione >= max(punti_crisi, punti_crescita):
            return "Espansione"
        elif punti_crescita >= max(punti_crisi, punti_espansione):
            return "Crescita"
        else:
            return "Crisi"
    except Exception as e:
        logging.error(f"Errore durante l'assegnazione della macro area: {e}")
        return "ND"
