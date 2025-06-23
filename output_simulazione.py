from utils import interpreta_macro_area, interpreta_mcc, interpreta_z_score
from query_supabase import recupera_dettagli_bando
from loguru import logger


def genera_output_simulazione(bandi_simulati, indici_simulati):
    if not bandi_simulati or not indici_simulati:
        return ""

    output = "\n\n\n⚙️ **Simulazione eVoluto: Potenziale accesso a bandi superiori**\n"
    output += f"- Nuova Macro Area simulata: **{indici_simulati.get('macro_area', '--')}** ({interpreta_macro_area(indici_simulati.get('macro_area'))})\n"
    output += f"- 🧮 Z-score simulato: {indici_simulati.get('z_score', '--')} ({interpreta_z_score(indici_simulati.get('z_score'))})\n"
    output += f"- 📊 MCC simulato: {indici_simulati.get('mcc_rating', '--')} ({interpreta_mcc(indici_simulati.get('mcc_rating'))})\n"

    output += "\n\n📊 **Indici simulati di supporto**\n"
    output += f"- ROE simulato: {indici_simulati.get('ROE', '--')}\n"
    output += f"- Debt/Equity simulato: {indici_simulati.get('Debt/Equity Ratio', '--')}\n"
    output += f"- Current Ratio simulato: {indici_simulati.get('Current Ratio', '--')}\n"
    output += f"- Quick Ratio simulato: {indici_simulati.get('Quick Ratio', '--')}\n"
    output += f"- Cash Ratio simulato: {indici_simulati.get('Cash Ratio', '--')}\n"
    output += f"- ROS simulato: {indici_simulati.get('ROS', '--')}\n"

    output += "\n\n📑 **Top 3 Bandi selezionati in base alla simulazione**\n"

    for i, bando in enumerate(bandi_simulati[:3], 1):
        ID_Incentivo = bando.get("ID_Incentivo")
        logger.info(f"▶️ Recupero dettagli simulati per ID_Incentivo: {ID_Incentivo}")

        if isinstance(ID_Incentivo, int) or (isinstance(ID_Incentivo, str) and ID_Incentivo.isdigit()):
            try:
                dettagli_estesi = recupera_dettagli_bando(int(ID_Incentivo))
                logger.info(f"✅ Dettagli simulati ottenuti per ID {ID_Incentivo}: {dettagli_estesi}")
                bando.update(dettagli_estesi)
            except Exception as e:
                logger.error(f"❌ Errore durante recupero dettagli simulati per ID {ID_Incentivo}: {e}")
        else:
            logger.warning(f"⚠️ ID_Incentivo simulato non valido o mancante: {ID_Incentivo}")

        output += f"\n🔹 **{i+1}. {bando.get('Titolo', '—')}** (ID: `{bando.get('ID_Incentivo', 'N/D')}`)\n"
        output += f"- 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '--')}\n"
        output += f"- 💶 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '--')} €\n"
        output += f"- 🧮 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '--')} €\n"
        output += f"- 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '--')}\n"
        output += f"- ⏳ Scadenza: {bando.get('Data_chiusura', '--')}\n"

        dettagli = bando.get("dettagli_gpt", {})
        output += f"- 📋 Dettagli: {dettagli.get('Descrizione', '—')}\n"
        output += f"- 🗓️ Note di apertura/chiusura: {dettagli.get('Note_di_apertura_chiusura', '—')}\n"
        output += f"- 🏢 Tipologia soggetto: {dettagli.get('Tipologia_Soggetto', '—')}\n"
        output += f"- 📊 Stanziamento incentivo: {dettagli.get('Stanziamento_incentivo', '—')} €\n"
        output += f"- 🌐 Verifica online: {dettagli.get('Link_istituzionale', '—')}\n"

    return output
