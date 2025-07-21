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
    # Tolleranza ±10% o ±1 (dove applicabile)
    fatturato_min = data["fatturato"] * 0.9
    fatturato_max = data["fatturato"] * 1.1
    ebitda_min = data["ebitda"] * 0.9
    ebitda_max = data["ebitda"] * 1.1
    utile_min = data["utile_netto"] * 0.9
    utile_max = data["utile_netto"] * 1.1
    patrimonio_min = data["patrimonio_netto"] * 0.9
    patrimonio_max = data["patrimonio_netto"] * 1.1
    z_score_min = data["z_score"] * 0.9
    z_score_max = data["z_score"] * 1.1
    dip_min = max(0, data["dipendenti"] - 1)
    dip_max = data["dipendenti"] + 1

    # Prima query: include regione
    query = (
        supabase_client.table("evoluto_data_center")
        .select("*")
        .eq("ateco", data["ateco"])
        .eq("regione", data["regione"])
        .eq("dimensione", data["dimensione"])
        .eq("forma_giuridica", data["forma_giuridica"])
        .eq("mcc_rating", data["mcc_rating"])
        .eq("obiettivo_azienda", data["obiettivo_azienda"])
        .eq("bandi_trovati", data["bandi_trovati"])
        .gte("fatturato", fatturato_min).lte("fatturato", fatturato_max)
        .gte("ebitda", ebitda_min).lte("ebitda", ebitda_max)
        .gte("utile_netto", utile_min).lte("utile_netto", utile_max)
        .gte("patrimonio_netto", patrimonio_min).lte("patrimonio_netto", patrimonio_max)
        .gte("z_score", z_score_min).lte("z_score", z_score_max)
        .gte("dipendenti", dip_min).lte("dipendenti", dip_max)
    )

    result = query.execute()
    records = result.data if result.data else []
    match_locale = True

    # Seconda query: senza regione
    if len(records) == 0:
        query = (
            supabase_client.table("evoluto_data_center")
            .select("*")
            .eq("ateco", data["ateco"])
            .eq("dimensione", data["dimensione"])
            .eq("forma_giuridica", data["forma_giuridica"])
            .eq("mcc_rating", data["mcc_rating"])
            .eq("obiettivo_azienda", data["obiettivo_azienda"])
            .eq("bandi_trovati", data["bandi_trovati"])
            .gte("fatturato", fatturato_min).lte("fatturato", fatturato_max)
            .gte("ebitda", ebitda_min).lte("ebitda", ebitda_max)
            .gte("utile_netto", utile_min).lte("utile_netto", utile_max)
            .gte("patrimonio_netto", patrimonio_min).lte("patrimonio_netto", patrimonio_max)
            .gte("z_score", z_score_min).lte("z_score", z_score_max)
            .gte("dipendenti", dip_min).lte("dipendenti", dip_max)
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
            "📊 Analisi Comparativa tra Aziende Simili:\n"
            "Non sono ancora disponibili benchmark da aziende con caratteristiche simili alla tua.\n"
            "Questa analisi contribuirà a creare un nuovo riferimento per il tuo settore."
        )
    elif locale:
        return (
            "📊 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state individuate {n} aziende con profilo simile al tuo (stesso settore, area geografica e struttura economico-finanziaria).\n"
            f"La probabilità media di approvazione riscontrata sui bandi selezionati è pari al {round(media,1)}%."
        )
    else:
        return (
            "📊 Analisi Comparativa tra Aziende Simili:\n"
            f"Sono state trovate {n} aziende simili per settore e struttura finanziaria, ma situate in regioni differenti.\n"
            f"La probabilità media di approvazione osservata è pari al {round(media,1)}% e resta un valore utile di riferimento."
        )
