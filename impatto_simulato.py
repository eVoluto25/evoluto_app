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
        return (
            f"💡 IMPATTO SIMULATO\n"
            f"- Indebitamento post: {indebitamento_post:,.0f} €\n"
            f"- EBITDA post: {ebitda_post:,.0f} €\n"
            f"- Utile netto post: {utile_post:,.0f} €\n"
            f"- Variazione EBITDA: {ebitda_imp:.1f}%\n"
            f"- Variazione utile netto: {utile_imp:.1f}%"
        )
    except Exception as e:
        return f"❌ Errore durante il calcolo dell'impatto simulato: {e}"

def simula_impatto_totale(dati_azienda: dict, top5_bandi: list) -> str:
    totale_contributo = 0
    totale_beneficio = 0
    for b in top5_bandi:
        try:
            spesa = float(b.get("spesa_ammessa_min", 0))
            intensita = float(b.get("intensita_aiuto", 0)) / 100
            contributo = spesa * intensita
            beneficio = contributo  # Placeholder: puoi raffinarlo
            totale_contributo += contributo
            totale_beneficio += beneficio
        except Exception as e:
            print(f"Errore nel calcolo impatto totale: {e}")
            continue

    return (
        f"📊 IMPATTO TOTALE SIMULATO\n"
        f"- Totale contributo ottenibile: {totale_contributo:,.2f} €\n"
        f"- Beneficio economico complessivo stimato: {totale_beneficio:,.2f} €"
    )
