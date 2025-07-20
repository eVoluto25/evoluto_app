import os
import supabase
from supabase import create_client
from datetime import datetime

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def salva_su_supabase(data):
    response = supabase_client.table("evoluto_data_center").insert(data).execute()
    return response

def cerca_analisi_simili(data):
    fatturato_min = data["fatturato"] * 0.9
    fatturato_max = data["fatturato"] * 1.1
    ebitda_min = data["ebitda"] * 0.9
    ebitda_max = data["ebitda"] * 1.1
    utile_min = data["utile_netto"] * 0.9
    utile_max = data["utile_netto"] * 1.1

    query = (
        supabase_client.table("evoluto_data_center")
        .select("probabilita_media_approvazione")
        .eq("ateco", data["ateco"])
        .eq("regione", data["regione"])
        .eq("dimensione", data["dimensione"])
        .gte("fatturato", fatturato_min).lte("fatturato", fatturato_max)
        .gte("ebitda", ebitda_min).lte("ebitda", ebitda_max)
        .gte("utile_netto", utile_min).lte("utile_netto", utile_max)
    )

    result = query.execute()
    records = result.data if result.data else []
    match_locale = True

    if len(records) == 0:
        query = (
            supabase_client.table("evoluto_data_center")
            .select("probabilita_media_approvazione")
            .eq("ateco", data["ateco"])
            .eq("dimensione", data["dimensione"])
            .gte("fatturato", fatturato_min).lte("fatturato", fatturato_max)
            .gte("ebitda", ebitda_min).lte("ebitda", ebitda_max)
            .gte("utile_netto", utile_min).lte("utile_netto", utile_max)
        )
        result = query.execute()
        records = result.data if result.data else []
        match_locale = False

    count = len(records)

    if count == 0 or not all("probabilita_media_approvazione" in r for r in records):
        return {
            "analisi_simili_trovate": 0,
            "probabilita_media": None,
            "messaggio": render_benchmark_message(0, None, False)
        }

    probabilita_media = sum([r["probabilita_media_approvazione"] for r in records]) / count

    return {
        "analisi_simili_trovate": count,
        "probabilita_media": round(probabilita_media, 1),
        "messaggio": render_benchmark_message(count, probabilita_media, match_locale)
    }

def render_benchmark_message(n, media, locale):
    if n == 0:
        return (
            "\u2728 Analisi Comparativa tra Aziende Simili:\n"
            "Non risultano ancora analisi effettuate da aziende con un profilo simile al tuo.\n"
            "La tua analisi sarà la prima a definire il benchmark di riferimento per il tuo settore."
        )
    elif locale:
        return (
            f"\u2728 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state individuate {n} aziende con caratteristiche simili alla tua (ATECO, regione, dimensione e struttura finanziaria entro ±10%).\n"
            f"La probabilità media di approvazione riscontrata sui bandi selezionati è del {round(media,1)}%."
        )
    else:
        return (
            f"\u2728 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state trovate {n} aziende simili per settore e struttura finanziaria in regioni differenti.\n"
            f"La probabilità media di approvazione riscontrata rimane indicativa e utile: {round(media,1)}%."
        )
