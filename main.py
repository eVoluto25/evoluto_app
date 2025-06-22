import json
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

# Modelli input
class Anagrafica(BaseModel):
    codice_ateco: Optional[str] = None
    regione: Optional[str] = None
    forma_giuridica: Optional[str] = None
    numero_dipendenti: Optional[int] = None
    attivita_prevalente: Optional[str] = None

class Bilancio(BaseModel):
    ricavi: Optional[float] = 0
    utile_netto: Optional[float] = 0
    ebitda: Optional[float] = 0
    totale_attivo: Optional[float] = 0
    immobilizzazioni: Optional[float] = 0
    ricavi_anno_prec: Optional[float] = None

class RisposteTest(BaseModel):
    crisi_impresa: Optional[str] = None
    sostegno_liquidita: Optional[str] = None
    sostegno_investimenti: Optional[str] = None
    transizione_ecologica: Optional[str] = None
    innovazione_ricerca: Optional[str] = None

class InputDati(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio
    risposte_test: RisposteTest

# Indicatori economico-finanziari
def stima_z_score(bilancio: Bilancio):
    if not bilancio.totale_attivo or bilancio.totale_attivo == 0:
        return 0
    return round((bilancio.ebitda + bilancio.utile_netto) / bilancio.totale_attivo, 2)

def stima_mcc(bilancio: Bilancio):
    if not bilancio.ricavi or bilancio.ricavi == 0:
        return 0
    return round((bilancio.utile_netto / bilancio.ricavi) * 100, 2)

def necessita_simulazione(z_score, mcc_rating):
    soglia_z = 2.5
    soglia_mcc = 7
    return z_score < soglia_z or mcc_rating < soglia_mcc

def genera_bilancio_simulato(bilancio: Bilancio, macro_area_attuale: str) -> Bilancio:
    bilancio_simulato = bilancio.copy()

    # STEP 1: Se sei in Crisi, prova a simulare il passaggio a Sviluppo
    if macro_area_attuale == "Crisi":
        # Aumenta EBITDA per spingere lo Z-score oltre 1.8
        if bilancio_simulato.ebitda < 0.1 * bilancio_simulato.totale_attivo:
            bilancio_simulato.ebitda = round(0.12 * bilancio_simulato.totale_attivo, 2)

        # Aumenta utile netto per ridurre MCC (verso 5)
        if bilancio_simulato.utile_netto < 0.07 * bilancio_simulato.ricavi:
            bilancio_simulato.utile_netto = round(0.08 * bilancio_simulato.ricavi, 2)

    # STEP 2: Se sei in Sviluppo, prova ad arrivare a Espansione
    elif macro_area_attuale == "Sviluppo":
        if bilancio_simulato.ebitda < 0.14 * bilancio_simulato.totale_attivo:
            bilancio_simulato.ebitda = round(0.18 * bilancio_simulato.totale_attivo, 2)

        if bilancio_simulato.utile_netto < 0.09 * bilancio_simulato.ricavi:
            bilancio_simulato.utile_netto = round(0.10 * bilancio_simulato.ricavi, 2)

    # In tutti i casi ritorna il bilancio simulato
    return bilancio_simulato

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

def assegna_macro_area(z_score: float, mcc_rating: float) -> str:
    if z_score >= 2.5 and mcc_rating <= 3:
        print("# Macro area assegnata: Espansione (z ≥ 2.5 e MCC ≤ 3)")
        return "Espansione"
    elif 1.8 <= z_score < 2.5 and 4 <= mcc_rating <= 6:
        print("# Macro area assegnata: Sviluppo (1.8 ≤ z < 2.5 e 4 ≤ MCC ≤ 6)")
        return "Sviluppo"
    else:
        print("# Macro area assegnata: Crisi (z < 1.8 o MCC ≥ 7)")
        return "Crisi"
    
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
            mappa = {
            "crisi_impresa": "Crisi d’impresa",
            "sostegno_liquidita": "Sostegno liquidità",
            "sostegno_investimenti": "Sostegno investimenti",
            "transizione_ecologica": "Transizione ecologica",
            "innovazione_ricerca": "Innovazione e ricerca"
            }
            
            temi_attivi = []
            for key, tema in mappa.items():
                valore = getattr(risposte_test, key, "C")
                if isinstance(valore, str) and valore.strip().upper() in ("A", "B"):
                    temi_attivi.append(tema)
            logger.info(f"🟦 Tematiche attive calcolate: {tematiche_attive}")
            return temi_attivi

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("[FASTAPI] Endpoint /analizza-azienda attivo e in ascolto")
    output_analisi = []
    logger.info("Dati ricevuti: %s", dati.json())

    try:
        if not dati.anagrafica or not dati.bilancio:
            logger.warning("⚠️ [VALIDAZIONE] Dati anagrafica o bilancio mancanti")
            raise HTTPException(status_code=400, detail="Dati incompleti")
    
        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)
        logger.info(f"📊 Z-Score calcolato: {z_score}, MCC rating calcolato: {mcc_rating}")

        input_dict = dati.dict()
        input_dict["mcc_rating"] = mcc_rating

        logger.info(f"[DEBUG] Input ricevuto completo: {input_dict}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione: {str(e)}")

        estendi_ricerca = False
        if z_score >= 0.2 and mcc_rating >= 7:
            logger.info(f"📌 Estendi ricerca: {estendi_ricerca} (Z-Score: {z_score}, MCC: {mcc_rating})")
            estendi_ricerca = True

        tematiche_attive = calcola_tematiche_attive(dati)
        logger.info(f"[DEBUG] Tematiche attive calcolate: {tematiche_attive}")

        bilanci_da_valutare = [{"tipo": "reale", "bilancio": dati.bilancio, "z_score": z_score, "mcc": mcc_rating}]
        logger.info(f"📊 Bilanci da valutare per simulazione: {bilanci_da_valutare}")

        dimensione = dimensione_azienda(dati.anagrafica)

        if necessita_simulazione(z_score, mcc_rating):
            macro_area_attuale = assegna_macro_area(z_score, mcc_rating)
            logger.info(f"🏁 Avvio simulazione: macro area attuale = {macro_area_attuale}")
            bilancio_simulato = genera_bilancio_simulato(dati.bilancio, macro_area_attuale)

            z_sim = stima_z_score(bilancio_simulato)
            mcc_sim = stima_mcc(bilancio_simulato)
            macro_area_sim = assegna_macro_area(z_sim, mcc_sim)
            logger.info(f"🎯 Macro-area simulata assegnata: {macro_area_sim}")


            azienda_simulata = {
                "codice_ateco": dati.anagrafica.codice_ateco,
                "regione": dati.anagrafica.regione,
                "dimensione": dimensione,
                "ebitda": bilancio_simulato.ebitda,
                "immobilizzazioni": bilancio_simulato.immobilizzazioni,
                "macro_area": macro_area_sim,
                "tematiche_attive": tematiche_attive
            }
            logger.info(f"📦 Azienda simulata creata: {azienda_simulata}")
            
            logger.info(f"📤 Avvio classificazione bandi con dati: azienda={azienda_simulata}, bilanci={bilanci_da_valutare}, tematiche={tematiche_attive}")
            bandi = recupera_bandi_filtrati(
                macro_area=macro_area_sim,
                codice_ateco=dati.anagrafica.codice_ateco,
                regione=dati.anagrafica.regione,
                forma_giuridica=dati.anagrafica.forma_giuridica
            )

            # 🔍 Estensione attiva per sfruttare anche bandi con altre forme
            top_bandi_sim = classifica_bandi_avanzata(bandi, azienda_simulata, tematiche_attive, estensione=True)
            logger.info(f"✅ Classificazione completata: {len(top_bandi_sim)} bandi selezionati")

            print(f"\n🧪 Top bandi da simulazione: {len(top_bandi_sim)}")
            print(f"   Titoli bandi simulati: {[b.get('Titolo', '---') for b in top_bandi_sim]}")

            output_analisi.append({
                "tipo": "simulato",
                "macro_area": macro_area_sim,
                "z_score": z_sim,
                "mcc": mcc_sim,
                "bandi": top_bandi_sim
            })

            # ✅ AGGIUNGIAMO ANCHE QUESTO
            bilanci_da_valutare.append({
                "tipo": "simulato",
                "bilancio": bilancio_simulato,
                "z_score": z_sim,
                "mcc": mcc_sim
            })

        # 🔁 Unione bandi reali + simulati (se vuoi prendere i migliori)
        top_bandi = []
        top_bandi = top_bandi + top_bandi_sim
        top_bandi = sorted(top_bandi, key=lambda b: b.get("punteggio_totale", 0), reverse=True)[:3]

        macro_area_attuale = assegna_macro_area(dati.bilancio, dati.mcc_rating)

        if necessita_simulazione(z_score, mcc_rating):
            bilancio_simulato = genera_bilancio_simulato(dati.bilancio, macro_area_attuale)
            z_sim = stima_z_score(bilancio_simulato)
            mcc_sim = stima_mcc(bilancio_simulato)
            bilanci_da_valutare.append({
                "tipo": "simulato",
                "bilancio": bilancio_simulato,
                "z_score": z_sim,
                "mcc": mcc_sim
            })

        output_analisi = []

        for item in bilanci_da_valutare:
            bilancio_corrente = item["bilancio"]
            z_score_corrente = item["z_score"]
            mcc_corrente = item["mcc"]

            macro_area = assegna_macro_area(dati.bilancio)
            dimensione = dimensione_azienda(dati.anagrafica)
            indici_plus = calcola_indici_plus(dati.bilancio)

            output_analisi.append({
                "tipo": item["tipo"],
                "macro_area": macro_area,
                "dimensione": dimensione,
                "mcc_rating": mcc_corrente,
                "z_score": z_score_corrente,
                "indici_plus": indici_plus,
                "bilancio": bilancio_corrente
            })

        bandi = recupera_bandi_filtrati(
            macro_area=macro_area,
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )    

        tematiche_attive = calcola_tematiche_attive(dati.risposte_test)

        azienda = {
            "codice_ateco": dati.anagrafica.codice_ateco,
            "regione": dati.anagrafica.regione,
            "dimensione": dimensione,
            "ebitda": dati.bilancio.ebitda,
            "immobilizzazioni": dati.bilancio.immobilizzazioni,
            "macro_area": macro_area,
            "tematiche_attive": tematiche_attive
        }
        
        top_bandi = classifica_bandi_avanzata(bandi, azienda, tematiche_attive, estensione=estendi_ricerca)
        
        numero_bandi_filtrati = len(bandi)
        
        print(f"📊 Bandi totali filtrati da Supabase: {len(bandi)}")
        print(f"📋 Titoli bandi recuperati: {[b.get('Titolo', '--') for b in bandi]}")

        totale_agevolazioni_macroarea = sum(
            float(b.get("Agevolazione_Concedibile_max", 0)) 
            for b in bandi 
            if isinstance(b.get("Agevolazione_Concedibile_max", 0), (int, float))
        )

        print(f"🏆 Top bandi selezionati: {len(top_bandi)}")
        print(f"🏷️ Titoli top bandi: {[b.get('Titolo', '--') for b in top_bandi]}")
        
        totale_agevolazioni_macroarea = sum(
            float(b.get("Agevolazione_Concedibile_max", 0) or 0)
            for b in top_bandi
            if isinstance(b.get("Agevolazione_Concedibile_max", 0), (int, float, str))
        )

        for bando in top_bandi[:3] or []:
            titolo = bando.get("Titolo") or bando.get("titolo") or "Bando senza titolo"
            dettagli_supabase = recupera_dettagli_bando(bando.get("ID_Incentivo", ""))
            bando["dettagli_gpt"] = dettagli_supabase

        # ✅ Costruzione dell’output testuale
        risultati_finali = []

        for analisi in bilanci_da_valutare:
            bilancio_corrente = analisi["bilancio"]
            z_score = analisi["z_score"]
            mcc_rating = analisi["mcc"]

            macro_area = assegna_macro_area(bilancio_corrente)
            dimensione = dimensione_azienda(dati.anagrafica)
            indici_plus = calcola_indici_plus(bilancio_corrente)

            top_bandi = classifica_bandi_filtrati(
                bilancio=bilancio_corrente,
                macro_area=macro_area,
                dimensione=dimensione,
                mcc_rating=mcc_rating,
                z_score=z_score,
               temi_attivi=calcola_tematiche_attive(dati.risposte_test)
            )

            output_finale = genera_output_finale(
                top_bandi,
                macro_area,
                dimensione,
                mcc_rating,
                z_score,
                numero_bandi_filtrati=len(top_bandi),
                totale_agevolazioni_macroarea=None,
                indici_plus=indici_plus
            )

            risultati_finali.append({
                "tipo": analisi["tipo"],
                "macro_area": macro_area,
                "macro_area_interpretata": interpreta_macro_area(macro_area),
                "dimensione": dimensione,
                "indice_z_evoluto": z_score,
                "indice_z_evoluto_interpretato": interpreta_z_score(z_score),
                "indice_mcc_evoluto": mcc_rating,
                "indice_mcc_evoluto_interpretato": interpreta_mcc(mcc_rating),
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
    output += f"\n Totale agevolazioni disponibili per aziende in **{macro_area}**: €{totale_agevolazioni_macroarea:,.0f}\n"
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
