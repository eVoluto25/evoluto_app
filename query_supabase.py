from supabase import create_client
import os

# Collegamento a Supabase tramite chiavi salvate su Render
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def recupera_bandi_filtrati(...):
    ...
    bandi = []
    for row in query_supabase(...):  # pseudocodice
        bandi.append({
            "ID_incentivo": row["ID_incentivo"],
            "Titolo": row["Titolo"],
            "Obiettivo_finalita": row["Obiettivo_finalita"],
            "Data_apertura": row["Data_apertura"],
            "Data_chiusura": row["Data_chiusura"],
            "Dimensione": row["Dimensione"],
            "Forma_agevolazione": row["Forma_agevolazione"],
            "Spesa_Ammessa_max": row["Spesa_Ammessa_max"],
            "Agevolazione_Concedibile_max": row["Agevolazione_Concedibile_max"],
            "Codici_ATECO": row["Codici_ATECO"],
            "Regioni": row["Regioni"]
        })
    return bandi
