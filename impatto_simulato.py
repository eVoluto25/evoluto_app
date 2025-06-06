# impatto_simulato.py

def calcola_impatto_simulato(bando: dict, azienda: dict) -> str:
    try:
        spesa_progetto = float(bando.get("spesa_ammessa_min", 0))
        contributo_perc = float(bando.get("intensita_aiuto", 0)) / 100
        contributo = spesa_progetto * contributo_perc

        indebitamento_attuale = float(azienda.get("indebitamento", 0))
        ebitda_attuale = float(azienda.get("ebitda", 0))
        utile_attuale = float(azienda.get("utile_netto", 0))

        # Simulazioni
        indebitamento_post = max(0, indebitamento_attuale - contributo)
        ebitda_post = ebitda_attuale + contributo
        utile_post = utile_attuale + contributo

        # Calcolo impatto percentuale
        ebitda_imp = ((ebitda_post - ebitda_attuale) / ebitda_attuale * 100) if ebitda_attuale else 0
        utile_imp = ((utile_post - utile_attuale) / utile_attuale * 100) if utile_attuale else 0

        # Report sintetico
        return f"""
