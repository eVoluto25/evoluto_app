
import supabase
from supabase import create_client
import os

# Connessione Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

def genera_output_gpt(id_azienda):
    # Recupera la riga corrispondente nella tabella verifica_aziendale
    response = supabase_client.table("verifica_aziendale").select("*").eq("id_azienda", id_azienda).execute()
    if not response.data or len(response.data) == 0:
        return "Nessun dato trovato per l'ID azienda fornito."

    row = response.data[0]

    # Costruzione del testo
    output = f"""🔎 **Analisi aziendale - {row.get('ragione_sociale', 'N/A')}**

📍 **Dati identificativi**
• Partita IVA: {row.get('partita_iva', 'N/A')}
• Codice ATECO: {row.get('codice_ateco', 'N/A')}
• Forma giuridica: {row.get('forma_giuridica', 'N/A')}
• Attività prevalente: {row.get('attivita_prevalente', 'N/A')}
• Città: {row.get('citta', 'N/A')}
• Provincia: {row.get('provincia', 'N/A')}
• Data di costituzione: {row.get('data_costituzione', 'N/A')}
• Numero di dipendenti: {row.get('numero_dipendenti', 'N/A')}
• Dimensione impresa: {row.get('dimensione_impresa', 'N/A')}
• Amministratore: {row.get('amministratore', 'N/A')}

📊 **Indici economico-finanziari**
• Fatturato annuo: €{row.get('fatturato', 'N/A')}
• Utile netto: €{row.get('utile_netto', 'N/A')}
• EBITDA: €{row.get('ebitda', 'N/A')}
• EBITDA Margin: {row.get('ebitda_margin', 'N/A')}%
• Spese R&S: €{row.get('spese_rs', 'N/A')}
• Costi ambientali: €{row.get('costi_ambientali', 'N/A')}
• Totale attivo: €{row.get('totale_attivo', 'N/A')}
• Disponibilità liquide: €{row.get('disponibilita_liquide', 'N/A')}
• Immobilizzazioni: €{row.get('immobilizzazioni', 'N/A')}
• Indebitamento: €{row.get('indebitamento', 'N/A')}
• Debt/Equity: {row.get('debt_equity', 'N/A')}
• Current Ratio: {row.get('current_ratio', 'N/A')}
• Interest Coverage Ratio: {row.get('interest_coverage_ratio', 'N/A')}

📈 **Indicatori strategici**
• Autofinanziamento: €{row.get('autofinanziamento', 'N/A')}
• Investimenti recenti: €{row.get('investimenti_recenti', 'N/A')}

🏷️ **Macro area assegnata:** {row.get('macroarea', 'N/A')}

📌 **Valutazione bandi**
• Punteggio di accesso: {row.get('punteggio_bando', 'N/A')}/100
• Classe: {row.get('classe_accesso', 'N/A')}

🗂️ **Bandi consigliati (massimo 10)**
"""

    # Recupero dei bandi associati da tabella bandi_disponibili
    bandi_ids = row.get("id_incentivo", [])
    if isinstance(bandi_ids, str):
        bandi_ids = bandi_ids.split(",") if bandi_ids else []

    if bandi_ids:
        bandi_response = supabase_client.table("bandi_disponibili").select("*").in_("id_bando", bandi_ids).order("punteggio", desc=True).limit(10).execute()
        bandi = bandi_response.data if bandi_response.data else []
        for bando in bandi:
            output += f"- {bando.get('titolo', 'Titolo non disponibile')} – [{bando.get('territorio', 'Territorio')}]({bando.get('link', '#')})\n"
    else:
        output += "Nessun bando compatibile trovato.\n"

    return output
