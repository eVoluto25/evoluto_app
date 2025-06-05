
def assegna_macroarea(indici: dict) -> str:
    # Valori soglia
    ebitda_margin = float(indici.get("ebitda_margin", 0))
    utile_netto = float(indici.get("utile_netto", 0))
    debt_equity = float(indici.get("debt_equity_ratio", 0))
    current_ratio = float(indici.get("current_ratio", 0))
    interest_coverage = float(indici.get("interest_coverage_ratio", 0))
    ammortamenti = float(indici.get("capacita_autofinanziamento", 0)) - utile_netto
    patrimonio = float(indici.get("totale_attivo", 1))
    immobilizzazioni = float(indici.get("immobilizzazioni", 0))
    spese_rs = float(indici.get("spese_r_s", 0))
    autofin = utile_netto + ammortamenti
    costi_ambientali = float(indici.get("costi_ambientali", 0))
    ebitda = float(indici.get("ebitda", 0))

    solidita = patrimonio / float(indici.get("totale_attivo", 1)) if patrimonio else 0
    incidenza_investimenti = immobilizzazioni / patrimonio if patrimonio else 0

    # Conteggio per ciascuna macroarea
    score_crisi = 0
    if current_ratio < 1:
        score_crisi += 1
    if debt_equity > 2:
        score_crisi += 1
    if interest_coverage < 1:
        score_crisi += 1
    if ebitda_margin < 0.05:
        score_crisi += 1
    if utile_netto < 0:
        score_crisi += 1

    score_crescita = 0
    if autofin > 0:
        score_crescita += 1
    if solidita > 0.2:
        score_crescita += 1
    if incidenza_investimenti > 0.2:
        score_crescita += 1
    if spese_rs > 0:
        score_crescita += 1

    score_espansione = 0
    if ebitda > 0:
        score_espansione += 1
    if spese_rs > 0:
        score_espansione += 1
    if incidenza_investimenti > 0.25:
        score_espansione += 1
    if costi_ambientali > 0:
        score_espansione += 1
    if ebitda_margin > 0.10:
        score_espansione += 1

    scores = {
        "Crisi": score_crisi,
        "Crescita": score_crescita,
        "Espansione": score_espansione
    }

    # Assegna sempre la macroarea con punteggio più alto
    return max(scores, key=scores.get)

def aggiorna_macroarea_supabase(supabase_client, id_verifica: str, macroarea: str):
    supabase_client.table("verifica_aziendale").update({
        "macroarea": macroarea
    }).eq("id_verifica", id_verifica).execute()
