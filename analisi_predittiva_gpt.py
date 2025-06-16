from validazione_online import valida_bando_online_mock

def analizza_benefici_bandi(bandi, azienda):
    analisi = []

    impatti_strategici = {
        "transizione ecologica": "migliora il posizionamento ESG e rende la struttura più sostenibile nel medio termine",
        "transizione digitale": "favorisce l’innovazione interna e ottimizza i processi aziendali",
        "digitalizzazione": "porta maggiore efficienza e competitività tramite strumenti tecnologici",
        "internazionalizzazione": "apre l'accesso a nuovi mercati esteri, aumentando la resilienza del fatturato",
        "sviluppo d’impresa": "rafforza la crescita organica e migliora la solidità operativa",
        "investimenti produttivi": "abilita nuovi asset strategici e migliora il margine operativo lordo",
        "innovazione e ricerca": "rafforza il vantaggio competitivo e l’attrattività nel lungo termine",
        "crisi": "permette un riequilibrio finanziario, migliorando il cash flow e riducendo il rischio d’impresa",
        "inclusione sociale": "rafforza la responsabilità d’impresa e l’integrazione in contesti locali"
    }

    for bando in bandi:
        titolo = bando.get("titolo", "Bando senza titolo")
        obiettivo = bando.get("Obiettivo_Finalita", "").lower()
        macro_area = azienda.get("macro_area", "").lower()

        testo = f"📌 **{titolo}** – "

        impatto = next(
            (descrizione for keyword, descrizione in impatti_strategici.items() if keyword in obiettivo),
            "ha potenziale strategico per rafforzare l’assetto aziendale"
        )

        if "crisi" in macro_area:
            introduzione = "In un contesto di fragilità economica, l’adozione di questo bando"
        elif "sviluppo" in macro_area:
            introduzione = "Questo bando può accompagnare la crescita aziendale"
        elif "espansione" in macro_area:
            introduzione = "Lo strumento selezionato sostiene l’espansione e l’apertura a nuove opportunità"
        else:
            introduzione = "L’incentivo selezionato"

        sintesi = f"{introduzione} {impatto}."

        # Limita a circa 80 parole
        parole = sintesi.split()
        if len(parole) > 80:
            sintesi = " ".join(parole[:80]) + "..."

        testo += sintesi
        analisi.append(testo)

    return analisi
