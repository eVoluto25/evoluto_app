import logging
from classificazione_macroarea import popola_verifica_aziendale

logging.basicConfig(level=logging.INFO)

def estrai_indici(dati_bilancio):
    try:
        logging.info("\u2705 Avvio calcolo indici economico-finanziari")

        ricavi = dati_bilancio.get("ricavi", 0)
        utile_netto = dati_bilancio.get("utile_netto", 0)
        ebitda = dati_bilancio.get("ebitda", 0)
        ebit = dati_bilancio.get("risultato_operativo", 0)
        oneri_finanziari = dati_bilancio.get("oneri_finanziari", 1)
        attivo_corrente = dati_bilancio.get("attivo_corrente", 1)
        passivo_corrente = dati_bilancio.get("passivo_corrente", 1)
        debiti_totali = dati_bilancio.get("debiti", 0)
        patrimonio_netto = dati_bilancio.get("patrimonio_netto", 1)
        totale_attivo = dati_bilancio.get("totale_attivo", 1)
        liquidita = dati_bilancio.get("liquidita", 0)
        immobilizzazioni = dati_bilancio.get("immobilizzazioni", 0)
        ammortamenti = dati_bilancio.get("ammortamenti", 0)
        costi_ricerca = dati_bilancio.get("costi_ricerca", 0)
        costi_servizi = dati_bilancio.get("costi_servizi", 0)
        immobilizzazioni_anno_precedente = dati_bilancio.get("immobilizzazioni_anno_precedente", 0)

        dati_indici = {
            # Anagrafica
            "codice_ateco": dati_bilancio.get("codice_ateco"),
            "forma_giuridica": dati_bilancio.get("forma_giuridica"),
            "partita_iva": dati_bilancio.get("partita_iva"),
            "attivita_prevalente": dati_bilancio.get("attivita_prevalente"),
            "provincia": dati_bilancio.get("provincia"),
            "citta": dati_bilancio.get("citta"),
            "data_costituzione": dati_bilancio.get("data_costituzione"),
            "numero_dipendenti": dati_bilancio.get("numero_dipendenti", 0),
            "dimensione_impresa": dati_bilancio.get("dimensione_impresa"),
            "amministratore": dati_bilancio.get("amministratore"),

            # Conto Economico
            "fatturato": ricavi,
            "utile_netto": utile_netto,
            "ebitda": ebitda,
            "ebitda_margin": round(ebitda / ricavi, 2) if ricavi else 0,
            "spese_r_s": costi_ricerca,
            "costi_ambientali_presenti": costi_servizi > 0,

            # Stato Patrimoniale
            "totale_attivo": totale_attivo,
            "liquidita": liquidita,
            "immobilizzazioni": immobilizzazioni,
            "indebitamento": debiti_totali,
            "debt_equity": round(debiti_totali / patrimonio_netto, 2) if patrimonio_netto else 0,
            "current_ratio": round(attivo_corrente / passivo_corrente, 2) if passivo_corrente else 0,
            "interest_coverage_ratio": round(ebit / oneri_finanziari, 2) if oneri_finanziari else 0,

            # Indicatori derivati
            "autofinanziamento": utile_netto + ammortamenti,
            "investimenti_recenti": round(immobilizzazioni - immobilizzazioni_anno_precedente, 2)
        }

        logging.info("\u2705 Indici calcolati con successo")

        popola_verifica_aziendale(dati_indici)

    except Exception as e:
        logging.error(f"\u274C Errore nel calcolo degli indici: {str(e)}")
