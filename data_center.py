# data_center.py
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

    # Primo tentativo: match con regione
    query = (
        supabase_client.table("evoluto_data_center")
        .select("compatibilita_percentuale")
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
        # Secondo tentativo: senza regione
        query = (
            supabase_client.table("evoluto_data_center")
            .select("compatibilita_percentuale")
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

    if count == 0:
        return {
            "analisi_simili_trovate": 0,
            "compatibilita_media": None,
            "messaggio": render_benchmark_message(0, None, False)
        }

    compatibilita_media = sum([r["compatibilita_percentuale"] for r in records]) / count

    return {
        "analisi_simili_trovate": count,
        "compatibilita_media": round(compatibilita_media, 1),
        "messaggio": render_benchmark_message(count, compatibilita_media, match_locale)
    }

def render_benchmark_message(n, media, locale):
    if n == 0:
        return (
            "\u2728 Analisi Comparativa tra Aziende Simili:\n"
            "Non risultano ancora analisi effettuate da aziende con un profilo simile al tuo.\n"
            "La tua analisi sar\u00e0 la prima a definire il benchmark di riferimento per il tuo settore."
        )
    elif locale:
        return (
            f"\u2728 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state individuate {n} aziende con caratteristiche simili alla tua (ATECO, regione, dimensione e struttura finanziaria entro \u00b110%).\n"
            f"La compatibilit\u00e0 media riscontrata con i bandi selezionati \u00e8 del {round(media,1)}%."
        )
    else:
        return (
            f"\u2728 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state trovate {n} aziende simili per settore e struttura finanziaria in regioni differenti.\n"
            f"La compatibilit\u00e0 media riscontrata rimane indicativa e utile: {round(media,1)}%."
        )
