from claude_fallback import invia_a_claude
from supabase_client import inserisci_diagnosi

# ...

@app.post("/score")
async def score(input: Request):
    payload = await input.json()
    azienda = payload.get("azienda")
    bando = payload.get("bando")

    # Analisi + Matching
    azienda.update(analizza_macroarea({**azienda.get("anagrafica", {}), **azienda.get("bilancio", {})}))
    azienda.update(match_bando(azienda, bando))
    risultato = calcola_score(bando, azienda)

    # Claude fallback se richiesto
    if risultato["forward_to_claude"]:
        fallback_data = {
            "azienda": azienda,
            "bando": bando,
            "score": risultato
        }
        claude_output = invia_a_claude(fallback_data)
        risultato["macroarea_validata_claude"] = claude_output.get("macroarea_validata")
        risultato["motivazione_claude"] = claude_output.get("motivazione")

    # Salvataggio su Supabase
    record = {
        "azienda_id": azienda.get("anagrafica", {}).get("codice_fiscale"),
        "bando_id": bando.get("ID_Incentivo"),
        "score": risultato.get("score"),
        "macroarea": azienda.get("macroarea_primaria"),
        "diagnostica": risultato,
    }
    inserisci_diagnosi("bandi_semplificata", record)

    return risultato
