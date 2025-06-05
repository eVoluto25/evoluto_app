
def calcola_valutazione(verifica: dict, bando: dict, macroarea: str) -> dict:
    punteggio = 0

    # A. Compatibilità con la Macro Area – 30%
    finalita = bando.get("obiettivo_finalita", "").lower()
    macro_parole = {
        "Crisi": ["crisi", "liquidità", "inclusione sociale"],
        "Crescita": ["start up", "sviluppo", "investimenti", "giovanile", "femminile"],
        "Espansione": ["internazionalizzazione", "transizione", "innovazione", "ricerca"]
    }
    parole_rilevanti = macro_parole.get(macroarea, [])
    match_count = sum(1 for p in parole_rilevanti if p in finalita)
    if match_count >= 2:
        punteggio += 30
    elif match_count == 1:
        punteggio += 15

    # B. Solidità Finanziaria – 25%
    solidita = 0
    if float(verifica.get("ebitda_margin", 0)) > 0.10:
        solidita += 1
    if float(verifica.get("utile_netto", 0)) > 0:
        solidita += 1
    debt_equity = float(verifica.get("debt_equity_ratio", 0))
    if 0.5 <= debt_equity <= 2:
        solidita += 1
    punteggio += solidita * (25 / 3)

    # C. Forma agevolazione – 15%
    forma = bando.get("forma_agevolazione", "").lower()
    if "fondo perduto" in forma:
        punteggio += 15
    elif "credito d’imposta" in forma or "credito imposta" in forma:
        punteggio += 8
    elif "finanziamento" in forma:
        punteggio += 4

    # D. Dimensione aziendale – 10%
    pmi = int(verifica.get("numero_dipendenti", 0)) <= 250 and float(verifica.get("fatturato_annuo", 0)) <= 50_000_000
    if pmi and "PMI" in bando.get("beneficiari", ""):
        punteggio += 10
    elif not pmi and "grande impresa" in bando.get("beneficiari", ""):
        punteggio += 10
    elif pmi:
        punteggio += 5

    # E. Capacità di co-finanziamento – 10%
    autofin = float(verifica.get("capacita_autofinanziamento", 0))
    utile = float(verifica.get("utile_netto", 0))
    if autofin > 0 or utile > 0:
        punteggio += 10

    # F. Territorio e ATECO – 10%
    ateco = verifica.get("codice_ateco", "").lower()
    provincia = verifica.get("provincia", "").lower()
    if provincia in bando.get("ambito_territoriale", "").lower():
        punteggio += 5
    if ateco in bando.get("beneficiari", "").lower():
        punteggio += 5

    # Classificazione qualitativa
    if punteggio >= 80:
        classe = "Alta"
    elif punteggio >= 50:
        classe = "Media"
    else:
        classe = "Bassa"

    return {
        "valutazione_0_100": str(int(punteggio)),
        "probabilità": classe
    }

def aggiorna_valutazione_supabase(supabase_client, id_verifica: str, valutazione: dict):
    supabase_client.table("verifica_aziendale").update({
        "valutazione_0_100": valutazione["valutazione_0_100"],
        "probabilità": valutazione["probabilità"]
    }).eq("id_verifica", id_verifica).execute()
