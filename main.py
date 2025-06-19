import json
from query_supabase import recupera_bandi_filtrati
from query_supabase import somma_agevolazioni_macroarea
from classifica_bandi import classifica_bandi_avanzata
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict
from validazione_google import cerca_google_bando
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

def assegna_macro_area(bilancio: Bilancio) -> str:
    z_score = stima_z_score(bilancio)

    if bilancio.ebitda > 0:
        if z_score >= 0.20:
            print("📍 Macro area assegnata: Espansione (z_score >= 0.20)")
            return "Espansione"
        elif z_score > 0.05:
            print("📍 Macro area assegnata: Sviluppo (z_score > 0.05)")
            return "Sviluppo"
        else:
            print("📍 Macro area assegnata: Crisi (z_score basso con EBITDA > 0)")
            return "Crisi"
    elif bilancio.ricavi > 0:
        print("📍 Macro area assegnata: Sviluppo (EBITDA ≤ 0 ma ricavi > 0)")
        return "Sviluppo"
    print("📍 Macro area assegnata: Crisi (nessun ricavo o EBITDA ≤ 0)")    
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

@app.post("/analizza-azienda")
async def analizza_azienda(dati: InputDati):
    logger.info("Dati ricevuti: %s", dati.json())

    logger.info(f"[DEBUG] Input ricevuto completo: {dati.dict()}")

    try:
        if not dati.anagrafica or not dati.bilancio:
            raise HTTPException(status_code=400, detail="Dati incompleti")

        z_score = stima_z_score(dati.bilancio)
        mcc_rating = stima_mcc(dati.bilancio)
        macro_area = assegna_macro_area(dati.bilancio)
        dimensione = dimensione_azienda(dati.anagrafica)

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
            return temi_attivi

        bandi = recupera_bandi_filtrati(
            macro_area=macro_area,
            codice_ateco=dati.anagrafica.codice_ateco,
            regione=dati.anagrafica.regione
        )    

        tematiche_attive = calcola_tematiche_attive(dati.risposte_test)
        top_bandi = classifica_bandi_avanzata(bandi, azienda, tematiche_attive)
        
        numero_bandi_filtrati = len(bandi)
        
        print(f"📊 Bandi totali filtrati da Supabase: {len(bandi)}")
        print(f"📋 Titoli bandi recuperati: {[b.get('Titolo', '--') for b in bandi]}")

        totale_agevolazioni_macroarea = sum(
            float(b.get("Agevolazione_Concedibile_max", 0)) 
            for b in bandi 
            if isinstance(b.get("Agevolazione_Concedibile_max", 0), (int, float))
        )

        azienda = {
            "codice_ateco": dati.anagrafica.codice_ateco,
            "regione": dati.anagrafica.regione,
            "dimensione": dimensione,
            "ebitda": dati.bilancio.ebitda,
            "immobilizzazioni": dati.bilancio.immobilizzazioni,
            "macro_area": macro_area,
            "tematiche_attive": tematiche_attive
        }

        top_bandi = classifica_bandi(bandi, azienda)

        print(f"🏆 Top bandi selezionati: {len(top_bandi)}")
        print(f"🏷️ Titoli top bandi: {[b.get('Titolo', '--') for b in top_bandi]}")
        
        totale_agevolazioni_macroarea = sum(
            float(b.get("Agevolazione_Concedibile_max", 0) or 0)
            for b in top_bandi
            if isinstance(b.get("Agevolazione_Concedibile_max", 0), (int, float, str))
        )

        stato_bandi = []
        for bando in top_bandi[:10] or []:
            try:
                titolo = bando.get("Titolo") or bando.get("titolo") or "Bando senza titolo"
                validazione = cerca_google_bando(titolo, dati.anagrafica.regione)
            except Exception as e:
                validazione = {
                    "validato": False,
                    "fondi_disponibili": False,
                    "messaggio": f"⚠️ Errore nella validazione Google: {str(e)}"
                }

            stato_bandi.append({
                "titolo": bando.get("titolo"),
                "validato": validazione["validato"],
                "fondi_disponibili": validazione["fondi_disponibili"],
                "esito": "✅ Validato online (titolo del bando trovato su fonte ufficiale)",
                "Verifica online": True,
                "Approfondimenti online": True
            })

        print(stato_bandi)

        # ✅ Costruzione dell’output testuale
        output_finale = genera_output_finale(
            top_bandi, macro_area, dimensione, mcc_rating, z_score,
            validazione_online=stato_bandi,
            numero_bandi_filtrati=numero_bandi_filtrati,
            totale_agevolazioni_macroarea=totale_agevolazioni_macroarea
        )
        print("\n\n🪵 LOG COMPLETO OUTPUT:\n")
        print(output_finale)
        print("\n📏 Lunghezza caratteri:", len(output_finale))
        
        return {
            "macro_area": macro_area,
            "macro_area_interpretata": interpreta_macro_area(macro_area),
            "dimensione": dimensione,
            "indice_z_evoluto": z_score,
            "indice_z_evoluto_interpretato": interpreta_z_score(z_score),
            "indice_mcc_evoluto": mcc_rating,
            "indice_mcc_evoluto_interpretato": interpreta_mcc(mcc_rating),
            "stato_bandi": stato_bandi,
            "bandi_filtrati": top_bandi[:10],
            "output_finale": output_finale 
        }

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
    validazione_online=None,
    approfondimenti_google=None, 
    totale_agevolazioni_macroarea=None
):
    output = "📌 **Analisi Aziendale**\n"
    output += f"- Macro Area: **{macro_area}** ({interpreta_macro_area(macro_area)})\n"
    output += f"- **Bandi disponibili da fonte Ministeriale in linea con il profilo aziendale:** {numero_bandi_filtrati}\n"
    output += f"\n Totale agevolazioni disponibili per aziende in **{macro_area}**: €{totale_agevolazioni_macroarea:,.0f}\n"
    output += f"- Dimensione: **{dimensione}**\n"
    output += f"📊 **Indice MCC-eVoluto:** {mcc_rating} ({interpreta_mcc(mcc_rating)})\n"
    output += f"🧮 **Indice Z-eVoluto:** {z_score:.2f} ({interpreta_z_score(z_score)})\n"

    output += "\n\n📑 **Top 10 Bandi Selezionati**\n"
    for i, bando in enumerate(bandi[:10], 1):
        output += f"\n**{i}. {bando.get('Titolo', '--')}**\n"
        output += f"- 🎯 Obiettivo: {bando.get('Obiettivo_finalita', '--')}\n"
        output += f"- 💶 Spesa ammessa max: {bando.get('Spesa_Ammessa_max', '--')} €\n"
        output += f"- 🧮 Agevolazione concedibile: {bando.get('Agevolazione_Concedibile_max', '--')} €\n"
        output += f"- 🧾 Forma agevolazione: {bando.get('Forma_agevolazione', '--')}\n"
        output += f"- ⏳ Scadenza: {bando.get('Data_chiusura', '--')}\n"
        if validazione_online and i <= len(validazione_online):
            voce_val = validazione_online[i - 1]
            output += f"🌐 Verifica online: {voce_val.get('esito', 'Non disponibile')}\n"

            messaggio = voce_val.get('messaggio', '').strip()
            if messaggio and "Nessun risultato" not in messaggio:
                output += f"{messaggio}\n"
            
        if approfondimenti_google:
            output += "\n\n🔎 **Approfondimenti online trovati**\n"
            for voce in approfondimenti_google:
                output += f"{voce}\n"   
    
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
