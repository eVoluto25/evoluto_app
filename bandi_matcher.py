
def calcola_match_bando(bando: dict, macroarea: str) -> dict:
    finalita = bando.get("obiettivo_finalita", "").lower()
    parole_chiave = {
        "Crisi": [
            "crisi d’impresa", "sostegno liquidità", "inclusione sociale"
        ],
        "Crescita": [
            "start up", "sviluppo d’impresa", "sostegno investimenti",
            "imprenditoria giovanile", "imprenditoria femminile"
        ],
        "Espansione": [
            "internazionalizzazione", "sviluppo d’impresa", "transizione ecologica",
            "innovazione", "ricerca"
        ]
    }.get(macroarea, [])

    if any(kw in finalita for kw in parole_chiave):
        return {
            "Titolo": bando.get("titolo", ""),
            "Link_istituzionale": bando.get("link", ""),
            "Ambito_territoriale": bando.get("ambito_territoriale", "")
        }
    return None

def esegui_matching(bandi: list, macroarea: str) -> list:
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
