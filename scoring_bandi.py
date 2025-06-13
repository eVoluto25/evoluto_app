import os
import logging
from datetime import datetime
from supabase import create_client
from dateutil.parser import parse

# Setup Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definizione pesi
PESI = {
    "macroarea": 30,
    "solidita": 25,
    "forma_agevolazione": 15,
    "dimensione": 10,
    "cofinanziamento": 10,
    "territorio_settore": 10
}

# Mapping finalità → macroaree
MAPPING_FINALITA_MACROAREA = {
    "Crisi d'impresa": "Crisi",
    "Sostegno liquidità": "Crisi",
    "Inclusione sociale": "Crisi",
    "Start up / Sviluppo d'impresa": "Crescita",
    "Sostegno investimenti": "Crescita",
    "Imprenditoria giovanile": "Crescita",
    "Imprenditoria femminile": "Crescita",
    "Internazionalizzazione": "Espansione",
    "Sviluppo d'impresa": "Espansione",
    "Transizione ecologica": "Espansione",
    "Innovazione e ricerca": "Espansione"
}

def normalizza_dimensione(val):
    if "micro" in val.lower():
        return "Microimpresa"
    elif "piccola" in val.lower():
        return "Piccola Impresa"
    elif "media" in val.lower():
        return "Media Impresa"
    elif "grande" in val.lower():
        return "Grande Impresa"
    return "Non classificabile"

def punteggio_macroarea(macroarea_azienda, finalita_bando):
    punteggio = 0
    for f in finalita_bando:
        if MAPPING_FINALITA_MACROAREA.get(f) == macroarea_azienda:
            punteggio += 1
    return round((punteggio / len(finalita_bando)) * PESI["macroarea"])

def punteggio_solidita(indici):
    punti = 0
    try:
        if float(indici.get("EBITDA Margin", "ND")) > 10:
            punti += 1
        if float(indici.get("Utile Netto", "ND")) > 0:
            punti += 1
        if 0.5 <= float(indici.get("Debt/Equity", "ND")) <= 2:
            punti += 1
    except:
        logger.warning("Dati solidità parziali o ND")
    return round((punti / 3) * PESI["solidita"])

def punteggio_agevolazione(forme):
    punteggio = 0
    priorita = {"Contributo/Fondo perduto": 3, "Agevolazione fiscale": 2, "Prestito/Anticipo rimborsabile": 1}
    for f in forme:
        punteggio = max(punteggio, priorita.get(f.strip(), 0))
    return round((punteggio / 3) * PESI["forma_agevolazione"])

def punteggio_dimensione(dim_azienda, dim_bando):
    return PESI["dimensione"] if dim_azienda in dim_bando else 0

def punteggio_cofinanziamento(capacita=True):
    return PESI["cofinanziamento"] if capacita else round(PESI["cofinanziamento"] / 2)

def punteggio_settore_territorio(codice_ateco, codici_bando):
    if "tutti" in codici_bando.lower():
        return PESI["territorio_settore"]
    codici = [c.strip() for c in codici_bando.split(";")]
    for c in codici:
        if codice_ateco.startswith(c):
            return PESI["territorio_settore"]
    return 0

def classifica_score(score):
    if score >= 80:
        return "Alta probabilità"
    elif score >= 50:
        return "Media probabilità"
    return "Bassa probabilità"

def valuta_bando(bando, azienda):
    try:
        score = 0
        score += punteggio_macroarea(azienda["macroarea"], json.loads(bando["Obiettivo_Finalita"]))
        score += punteggio_solidita(azienda["indici"])
        score += punteggio_agevolazione(json.loads(bando["Forma_agevolazione"]))
        score += punteggio_dimensione(azienda["dimensione"], json.loads(bando["Dimensioni"]))
        score += punteggio_cofinanziamento(azienda.get("capacita_cofinanziamento", True))
        score += punteggio_settore_territorio(azienda["codice_ateco"], bando["Codici_ATECO"])
        return score, classifica_score(score)
    except Exception as e:
        logger.error(f"Errore valutazione bando {bando.get('Titolo', '')}: {e}")
        return 0, "Errore"

def filtra_e_valuta_bandi(macroarea, indici, azienda, bandi):
    bandi_filtrati = []
    for bando in bandi:
        punteggio = 0
        if macroarea == "Crisi":
            if indici.get("Debt/Equity") and 0.5 <= indici["Debt/Equity"] <= 2:
                punteggio += 1
            if indici.get("EBITDA Margin", 0) > 0:
                punteggio += 1
            if azienda.get("utile_netto", 0) > 0:
                punteggio += 1
        elif macroarea == "Crescita":
            if azienda.get("autofinanziamento", False):
                punteggio += 1
            if azienda.get("solidita_patrimoniale", False):
                punteggio += 1
            if azienda.get("investimenti_presenti", False):
                punteggio += 1
        elif macroarea == "Espansione":
            if azienda.get("fatturato_crescita", False):
                punteggio += 1
            if indici.get("ROS", 0) > 0.05:
                punteggio += 1
            if indici.get("EBITDA Margin", 0) > 0.1:
                punteggio += 1
        if punteggio >= 2:
            bandi_filtrati.append({**bando, "punteggio": punteggio})
    return sorted(bandi_filtrati, key=lambda b: b["punteggio"], reverse=True)
