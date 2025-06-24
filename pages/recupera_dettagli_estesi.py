# pages/recupera_dettagli_estesi.py

from query_supabase import supabase

def recupera_dettagli_estesi(ID_Incentivo: str, forma_giuridica_azienda: str) -> dict:
    try:
        response = supabase.table("bandi_disponibili") \
            .select("*") \
            .eq("ID_Incentivo", ID_Incentivo) \
            .single() \
            .execute()
        
        return response.data or {}
    except Exception as e:
        print(f"❌ Errore nel recupero dettagli estesi per ID {ID_Incentivo}: {e}")
        return {}
