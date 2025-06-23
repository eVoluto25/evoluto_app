from logica_macroarea import assegna_macro_area
from classifica_bandi import classifica_bandi_avanzata
from main import stima_z_score, stima_mcc
from recupera_bandi import recupera_bandi_filtrati

def necessita_simulazione(z_score, mcc_rating):
    soglia_z = 2.5
    soglia_mcc = 7
    return z_score < soglia_z or mcc_rating < soglia_mcc


def genera_bilancio_simulato(bilancio, macro_area_attuale: str):
    bilancio_simulato = bilancio.copy()

    # STEP 1: Se sei in Crisi, prova a simulare il passaggio a Sviluppo
    if macro_area_attuale == "Crisi":
        # Aumenta EBITDA per spingere lo Z-score oltre 1.8
        if bilancio_simulato.ebitda < 0.1 * bilancio_simulato.totale_attivo:
            bilancio_simulato.ebitda = round(0.12 * bilancio_simulato.totale_attivo, 2)

        # Aumenta utile netto per ridurre MCC (reverse Debt/Equity)
        if bilancio_simulato.utile_netto < 0:
            bilancio_simulato.utile_netto = 30000

    # STEP 2: Se sei in Sviluppo, prova a passare a Transizione
    elif macro_area_attuale == "Sviluppo":
        if bilancio_simulato.ebitda < 0.15 * bilancio_simulato.totale_attivo:
            bilancio_simulato.ebitda = round(0.18 * bilancio_simulato.totale_attivo, 2)

        if bilancio_simulato.utile_netto < 0.03 * bilancio_simulato.ricavi:
            bilancio_simulato.utile_netto = round(0.06 * bilancio_simulato.ricavi, 2)

    return bilancio_simulato


def esegui_simulazione(bilancio_corrente, codice_ateco, regione, dimensione, tematiche_attive, macro_area_attuale):
    # 1. Genera bilancio simulato coerente con l’area attuale
    bilancio_sim = genera_bilancio_simulato(bilancio_corrente, macro_area_attuale)

    # 2. Calcola rating simulato
    z_sim, mcc_sim = calcola_rating_mcc_zscore(bilancio_sim)

    # 3. Nuova macro area
    macro_area_sim = assegna_macro_area(z_sim, mcc_sim)

    # 4. Costruzione profilo simulato
    azienda_sim = {
        "bilancio": bilancio_sim,
        "macro_area": macro_area_sim,
        "dimensione": dimensione,
        "mcc_rating": mcc_sim,
        "z_score": z_sim
    }

    # 5. Recupera e classifica bandi
    bandi_sim = recupera_bandi_filtrati(
        macro_area=macro_area_sim,
        codice_ateco=codice_ateco,
        regione=regione
    )

    top_bandi_sim = classifica_bandi_avanzata(
        bandi_sim,
        azienda_sim,
        tematiche_attive,
        estensione=True
    )

    return {
    "macro_area": macro_area_sim,
    "z_score": z_sim,
    "mcc_rating": mcc_sim,
    "dimensione": dimensione,
    "output": output,
    "top_bandi": top_bandi_sim,
    "indici_plus": calcola_indici_plus(bilancio_simulato)
}
