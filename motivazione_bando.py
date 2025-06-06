# motivazione_bando.py

def genera_motivazione(bando):
    motivazioni = []

    if bando.get("match_macroarea", False):
        motivazioni.append("perfettamente allineato con la tua macroarea")

    if bando.get("compatibilita_finanziaria", 0) >= 20:
        motivazioni.append("ottima solidità finanziaria rilevata")

    if "fondo perduto" in bando.get("forma_agevolazione", "").lower():
        motivazioni.append("prevede un contributo a fondo perduto elevato")

    if bando.get("beneficio_stimato", 0) > 0:
        motivazioni.append("offre un beneficio economico rilevante")

    if not motivazioni:
        return "Scelto per buona compatibilità complessiva con il tuo profilo aziendale."

    return "Scelto perché " + ", ".join(motivazioni) + "."
