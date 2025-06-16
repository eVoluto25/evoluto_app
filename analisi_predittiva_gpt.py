
def analizza_benefici_bandi(bandi, azienda):
    analisi = []

    for bando in bandi:
        titolo = bando.get("titolo", "Bando senza titolo")
        obiettivo = bando.get("Obiettivo_Finalita", "").lower()
        forma = bando.get("Forma_agevolazione", "").lower()
        agevolazione = bando.get("Agevolazione_Concedibile_max", 0)
        spesa = bando.get("Spesa_Ammessa_max", 0)
        ebitda = azienda.get("ebitda", 0)
        immobilizzazioni = azienda.get("immobilizzazioni", 0)
        macro_area = azienda.get("macro_area", "")

        impatto = []

        # 1. Patrimoniale / reddituale
        if "fondo perduto" in forma or "contributo" in forma:
            impatto.append("potenzia la struttura patrimoniale aziendale")
        elif "prestito" in forma:
            impatto.append("fornisce liquidità ma impatta sul debito")

        # 2. Coerenza con macro area
        if "sviluppo" in obiettivo and "Sviluppo" in macro_area:
            impatto.append("coerente con l'espansione e lo sviluppo operativo")
        elif "crisi" in obiettivo and "Crisi" in macro_area:
            impatto.append("mirato alla ristrutturazione aziendale")
        elif "internazionalizzazione" in obiettivo and "Espansione" in macro_area:
            impatto.append("utile per l'apertura a nuovi mercati")

        # 3. Sostenibilità economica
        if agevolazione <= ebitda * 0.3:
            impatto.append("sostenibile rispetto alla marginalità")
        elif spesa <= immobilizzazioni:
            impatto.append("compatibile con l'attivo immobilizzato")

        sintesi = f"📌 **{titolo}** – " + "; ".join(impatto) + "."

        analisi.append(sintesi)

    return analisi
