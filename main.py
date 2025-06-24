import json
from fastapi import Request
from models import Bilancio, Anagrafica, RisposteTest, InputDati
from query_supabase import recupera_dettagli_bando
from query_supabase import recupera_bandi_filtrati
from query_supabase import somma_agevolazioni_macroarea
from classifica_bandi import classifica_bandi_avanzata
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict
from indicatori import converti_z_score_lettera, converti_mcc_lettera
from indicatori import stima_z_score, stima_mcc
from logica_macroarea import assegna_macro_area
from output_simulazione import genera_output_simulazione
from simulazione_analisi import necessita_simulazione, genera_bilancio_simulato
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def root():
    return "eVoluto è attivo."

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://evoluto.capitaleaziendale.it"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def calcola_indici_plus(bilancio: Bilancio) -> dict:
    try:
        patrimonio_netto = bilancio.totale_attivo - sum([
            bilancio.immobilizzazioni,
            getattr(bilancio, "debiti", 0)
        ])
    except:
        patrimonio_netto = 0

    def safe_div(num, den):
        try:
            if den == 0: return "ND"
            return round(num / den, 2)
        except:
            return "ND"

    ricavi_giornalieri = safe_div(bilancio.ricavi, 365)

    return {
        "ROE": safe_div(bilancio.utile_netto, patrimonio_netto),
        "Debt/Equity Ratio": safe_div(getattr(bilancio, "debiti", 0), patrimonio_netto),
        "Current Ratio": safe_div(getattr(bilancio, "attivo_circolante", 0), getattr(bilancio, "passivo_corrente", 0)),
        "DSO": safe_div(getattr(bilancio, "crediti_vs_clienti", 0), ricavi_giornalieri),
        "Quick Ratio": safe_div(getattr(bilancio, "crediti_vs_clienti", 0) + getattr(bilancio, "liquidita", 0), getattr(bilancio, "passivo_corrente", 0)),
        "Cash Ratio": safe_div(getattr(bilancio, "liquidita", 0), getattr(bilancio, "passivo_corrente", 0)),
        "ROS": safe_div(getattr(bilancio, "ebit", 0), bilancio.ricavi)
    }

def interpreta_macro_area(macro_area: str) -> str:
    if macro_area == "Espansione":
        return "🚀 Fase di crescita: investimenti e sviluppo"
    elif macro_area == "Sviluppo":
        return "📈 Fase di consolidamento e ottimizzazione"
    elif macro_area == "Crisi":
        return "⚠️ Stato critico: rilancio e risanamento"
    return "⚙️ Stato non classificato"

def dimensione_azienda(anagrafica: Anagrafica) -> str:
    if anagrafica.numero_dipendenti is None:
        return "Non classificabile"
    if anagrafica.numero_dipendenti <= 9:
        return "Microimpresa"
    elif anagrafica.numero_dipendenti <= 49:
        return "Piccola Impresa"
    elif anagrafica.numero_dipendenti <= 249:
        return "Media Impresa"
    return "Grande impresa"

def calcola_tematiche_attive(risposte_test: RisposteTest):
    logger.info(">>> Debug: entrato in calcola_tematiche_attive")

    risposte_dict = risposte_test.dict()
    temi_attivi = []

    for key, valore in risposte_dict.items():
        logger.info(f">>> Debug: key={key}, valore={valore}")
        if isinstance(valore, str) and valore.strip().upper() in ("A", "B"):
            temi_attivi.append(key)

    return temi_attivi

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("Dati ricevuti: %s", dati.json())

    try:
        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)
        print(f">>> Z-Score calcolato: {z_score}")
        print(f">>> MCC calcolato: {mcc_rating}")
        logger.info(f">>> Z-Score calcolato: {z_score}")
        logger.info(f">>> MCC calcolato: {mcc_rating}")
    
        if not dati.anagrafica or not dati.bilancio:
            raise HTTPException(status_code=400, detail="Dati incompleti")

        input_dict = dati.dict()
        risposte_test_dict = dati.risposte_test.dict()
        for key, value in risposte_test_dict.items():
            logger.info(f">>> Risposta test - {key}: {value}")
            
        input_dict["mcc_rating"] = mcc_rating
        input_dict["z_score"] = z_score
        logger.info(f"[DEBUG] Input ricevuto completo: {input_dict}")
        print(">>> Debug: input_dict completato e pronto")
        logger.info(">>> Debug: input_dict completato e pronto")

        estendi_ricerca = False
        if z_score >= 0.2 and mcc_rating >= 7:
            estendi_ricerca = True

        tematiche_attive = calcola_tematiche_attive(dati)
        print(">>> Debug: calcolate tematiche attive")
        logger.info(">>> Debug: calcolate tematiche attive")

        bilanci_da_valutare = [{
            "tipo": "reale",
            "bilancio": dati.bilancio,
            "z_score": z_score,
            "z_score_letter": converti_z_score_lettera(z_score),
            "mcc": mcc_rating,
            "mcc_letter": converti_mcc_lettera(mcc_rating),
        }]
        
        dimensione = dimensione_azienda(dati.anagrafica)
        macro_area_attuale = assegna_macro_area(z_score, mcc_rating)
        
        risultati_finali = []

        # === ANALISI SIMULATA BASATA SU RISPOSTE TESTUALI ===
       
        bandi_simulati = recupera_bandi_filtrati(
            macro_area="espansione",  # default placeholder
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )
        
        print(f">>> Debug: risposte_test è {type(dati.risposte_test)}")
        print(f">>> Debug: contenuto = {dati.risposte_test}")
        
        output_simulato = genera_output_simulazione(dati.risposte_test.dict(), bandi_simulati)

        if isinstance(output_simulato, dict):
            risultati_finali.append(output_simulato)
            logger.info(">>> Output simulazione testuale aggiunto ai risultati finali")

        for analisi in bilanci_da_valutare:
            print(f">>> Analisi tipo: {analisi['tipo']}")
            bilancio_corrente = analisi["bilancio"]
            z_score = analisi["z_score"]
            mcc_rating = analisi["mcc"]

            # Conversione in lettere
            z_score_lettera = converti_z_score_lettera(z_score)
            mcc_lettera = converti_mcc_lettera(mcc_rating)

            # Macro area
            macro_area = assegna_macro_area(z_score, mcc_rating)
            dimensione = dimensione_azienda(dati.anagrafica)
            indici_plus = calcola_indici_plus(bilancio_corrente)

            bandi = recupera_bandi_filtrati(
                macro_area=macro_area,
                codice_ateco=dati.anagrafica.codice_ateco,
                regione=dati.anagrafica.regione
            )

            azienda = {
                "bilancio": bilancio_corrente,
                "macro_area": macro_area,
                "dimensione": dimensione,
                "mcc_rating": mcc_rating,
                "z_score": z_score
            }

            top_bandi = classifica_bandi_avanzata(
                bandi,
                azienda,
                tematiche_attive,
                estensione=True
            )

            for bando in top_bandi[:3]:
                dettagli_supabase = recupera_dettagli_bando(bando.get("ID_Incentivo", ""))
                bando["dettagli_gpt"] = dettagli_supabase

            output_finale = genera_output_finale(
                bandi=top_bandi,
                macro_area=macro_area,
                dimensione=dimensione,
                mcc_rating=mcc_rating,
                z_score=z_score,
                numero_bandi_filtrati=len(top_bandi),
                totale_agevolazioni_macroarea=None,
                indici_plus=indici_plus
            )

            risultati_finali.append({
                "tipo": analisi["tipo"],
                "macro_area": macro_area,
                "macro_area_interpretata": interpreta_macro_area(macro_area),
                "dimensione": dimensione,
                "z_score": z_score,
                "z_score_lettera": z_score_lettera,
                "z_score_interpretato": interpreta_z_score(z_score),
                "mcc_rating": mcc_rating,
                "mcc_lettera": mcc_lettera,
                "mcc_rating_interpretato": interpreta_mcc(mcc_rating),
                "bandi_filtrati": top_bandi[:3],
                "output_finale": output_finale,
                "indici_plus": indici_plus
            })

            return risultati_finali

    except Exception as e:
        logger.exception("Errore durante l'elaborazione")
        raise HTTPException(status_code=500, detail=str(e))
        
def interpreta_z_score(z):
    if z > 0.20:
        return "✅ Eccellente"
    elif z > 0.10:
        return "🟡 Buona"
    elif z > 0.00:
        return "🟠 Debole"
    return "🔴 Critica"

def interpreta_mcc(mcc):
    if mcc > 10:
        return "✅ Molto solida"
    elif mcc > 5:
        return "🟢 Buona"
    elif mcc > 1:
        return "🟡 Sufficiente"
    return "🔴 Critica"


# OUTPUT TESTUALE GPT
def genera_output_finale(
    bandi,
    macro_area,
    dimensione,
    mcc_rating,
    z_score,
    numero_bandi_filtrati,
    totale_agevolazioni_macroarea=None,
    indici_plus=None
):
    output = "📌 **Analisi Aziendale**\n"
    output += f"- Macro Area: **{macro_area}** ({interpreta_macro_area(macro_area)})\n"
    output += f"- **Bandi disponibili da fonte Ministeriale in linea con il profilo aziendale:** {numero_bandi_filtrati}\n"
    output += f"\n Totale agevolazioni disponibili per aziende in **{macro_area}**: €{(totale_agevolazioni_macroarea or 0):.0f}\n"
    output += f"- Dimensione: **{dimensione}**\n"
    output += f"📊 **Indice MCC-eVoluto:** {mcc_rating} ({interpreta_mcc(mcc_rating)})\n"
    output += f"🧮 **Indice Z-eVoluto:** {z_score:.2f} ({interpreta_z_score(z_score)})\n"
    output += f"\n\n📊 **Indici extra di supporto**\n"
    output += f"- ROE (Return on Equity): {indici_plus.get('ROE', 'Non disponibile')}\n"
    output += f"- Debt/Equity Ratio: {indici_plus.get('Debt/Equity Ratio', 'Non disponibile')}\n"
    output += f"- Current Ratio: {indici_plus.get('Current Ratio', 'Non disponibile')}\n"
    output += f"- DSO (Days Sales Outstanding): {indici_plus.get('DSO', 'Non disponibile')}\n"
    output += f"- Quick Ratio: {indici_plus.get('Quick Ratio', 'Non disponibile')}\n"
    output += f"- Cash Ratio: {indici_plus.get('Cash Ratio', 'Non disponibile')}\n"
    output += f"- ROS (Return on Sales): {indici_plus.get('ROS', 'Non disponibile')}\n"

        # BLOCCO OPZIONALE PER SIMULAZIONE
    if indici_plus.get("simulazione"):

        output += "\n\n📈 **Simulazione eVoluto: Potenziale accesso a bandi superiori**\n"
        output += f"- Nuova Macro Area simulata: **{indici_plus['simulazione'].get('macro_area', '--')}**\n"
        output += f"- 🧮 Z-score simulato: {indici_plus['simulazione'].get('z_score', '--')}\n"
        output += f"- 📊 MCC simulato: {indici_plus['simulazione'].get('mcc_rating', '--')}\n"

        output += "\n📊 **Indici simulati di supporto**\n"
        output += f"- ROE simulato: {indici_plus['simulazione'].get('ROE', '—')}\n"
        output += f"- Debt/Equity simulato: {indici_plus['simulazione'].get('Debt/Equity Ratio', '—')}\n"
        output += f"- Current Ratio simulato: {indici_plus['simulazione'].get('Current Ratio', '—')}\n"
        output += f"- Quick Ratio simulato: {indici_plus['simulazione'].get('Quick Ratio', '—')}\n"
        output += f"- Cash Ratio simulato: {indici_plus['simulazione'].get('Cash Ratio', '—')}\n"
        output += f"- ROS simulato: {indici_plus['simulazione'].get('ROS', '—')}\n"

        # ▶️ Output bandi simulati
        output += genera_output_simulazione(
            bandi_simulati=indici_plus["simulazione"].get("bandi", []),
            indici_simulati=indici_plus["simulazione"]
        )

    output += "\n\n📑 **Top 3 Bandi Selezionati**\n"
    
    for i, bando in enumerate(bandi[:3], 1):
        ID_Incentivo = bando.get("ID_Incentivo")
        logger.info(f"▶️ Recupero dettagli per ID_Incentivo: {ID_Incentivo}")

        if isinstance(ID_Incentivo, int) or (isinstance(ID_Incentivo, str) and ID_Incentivo.isdigit()):
            try:
                dettagli_estesi = recupera_dettagli_bando(int(ID_Incentivo))
                logger.info(f"✅ Dettagli ottenuti per ID {ID_Incentivo}: {dettagli_estesi}")
                bando.update(dettagli_estesi)
            except Exception as e:
                logger.error(f"❌ Errore durante il recupero dettagli per ID {ID_Incentivo}: {e}")
        else:
            logger.warning(f"⚠️ ID_Incentivo non valido o mancante: {ID_Incentivo}")
        output += f"\n🔹 **{i+1}. {bando.get('Titolo', '—')}** (ID: `{bando.get('ID_Incentivo', 'N/D')}`)\n"
        output += f"- 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '--')}\n"
        output += f"- 💶 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '--')} €\n"
        output += f"- 🧮 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '--')} €\n"
        output += f"- 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '--')}\n"
        output += f"- ⏳ Scadenza: {bando.get('Data_chiusura', '--')}\n"
        # ✅ Inclusione dei dettagli estesi (dettagli_gpt)
        dettagli = bando.get("dettagli_gpt", {})
        output += f"- 📋 Dettagli: {dettagli.get('Descrizione', '—')}\n"
        output += f"- 🗓️ Note di apertura/chiusura: {dettagli.get('Note_di_apertura_chiusura', '—')}\n"
        output += f"- 🏢 Tipologia soggetto: {dettagli.get('Tipologia_Soggetto', '—')}\n"
        output += f"- 📊 Stanziamento incentivo: {dettagli.get('Stanziamento_incentivo', '—')} €\n"
        output += f"- 🌐 Verifica online: {dettagli.get('Link_istituzionale', '—')}\n"
        
        return output or ""

    # Endpoint di controllo per uptime
    @app.head("/ping")
    @app.get("/ping")
    async def ping(request: Request):
        return {"status": "ok"}

    # Avvio del server in modalità standalone
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000)
