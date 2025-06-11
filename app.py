import gradio as gr
import openai
import os
import pdfplumber
from fpdf import FPDF
import re
import csv
import io
import pandas as pd
from logger import log_info, log_error
from datetime import datetime, timedelta
from supabase import create_client, Client

# === Supabase client ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === Estrazione e normalizzazione PDF ===
def normalizza_valore(v):
    try:
        return float(re.sub(r"[^\d\-,]", "", v).replace(".", "").replace(",", "."))
    except:
        return 0.0

def estrai_dati(pdf_file):
    financials = {
        "utile_netto": 0,
        "patrimonio_netto": 0,
        "vendite": 0,
        "totale_attivo": 0,
        "risultato_operativo": 0,
        "oneri_finanziari": 0,
        "ammortamenti": 0,
        "debiti": 0,
        "disponibilita_liquide": 0,
        "rimanenze": 0,
        "attivita_breve": 0,
        "passivita_breve": 0,
        "flusso_cassa": 100000,
        "regione": "Calabria",
        "codice_ateco": "68.1",
        "dipendenti": 7,
        "investimenti": True,
        "autofinanziamento": True,
        "fatturato_crescita": True
    }

    mappa = {
        "Utile (perdita) dell'esercizio": "utile_netto",
        "Totale patrimonio netto": "patrimonio_netto",
        "ricavi delle vendite": "vendite",
        "Totale attivo": "totale_attivo",
        "Differenza tra valore e costi della produzione": "risultato_operativo",
        "interessi e altri oneri finanziari": "oneri_finanziari",
        "ammortamento": "ammortamenti",
        "Totale debiti": "debiti",
        "Disponibilità liquide": "disponibilita_liquide",
        "Rimanenze": "rimanenze",
        "Attivo circolante": "attivita_breve",
        "Passività correnti": "passivita_breve"
    }

    with pdfplumber.open(pdf_file.name) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for riga in text.split("\n"):
                for chiave, campo in mappa.items():
                    if chiave.lower() in riga.lower():
                        valori = re.findall(r"[-+]?\d[\d\.\,]*", riga)
                        if valori:
                            financials[campo] = normalizza_valore(valori[-1])

    return financials

# === Calcolo indici ===
def calcola_indici(d):
    ci = d["totale_attivo"] - d["disponibilita_liquide"]
    mol = d["risultato_operativo"] + d["ammortamenti"]
    pfn = d["debiti"] - d["disponibilita_liquide"]

    return {
        "EBITDA Margin": mol / d["vendite"] if d["vendite"] else 0,
        "ROE": d["utile_netto"] / d["patrimonio_netto"] if d["patrimonio_netto"] else 0,
        "Debt/Equity": d["debiti"] / d["patrimonio_netto"] if d["patrimonio_netto"] else 0,
        "EBIT/OF": d["risultato_operativo"] / d["oneri_finanziari"] if d["oneri_finanziari"] else 0,
        "PFN/MOL": pfn / mol if mol else 0,
        "vendite": d["vendite"],
        "totale_attivo": d["totale_attivo"]
    }

# === Assegnazione macroarea ===
MACROAREA_KEYWORDS = {
    "Crisi": ["crisi", "liquidità", "inclusione sociale"],
    "Crescita": ["startup", "sviluppo", "investimenti", "imprenditoria"],
    "Espansione": ["internazionalizzazione", "transizione", "innovazione", "ricerca"]
}

def assegna_macroarea(financials):
    return "Espansione"  # placeholder per logica reale

# === Scoring bandi ===
def valuta_bando(bando, macroarea, indici, azienda):
    score = 0

    # A - Macroarea (30)
    finalita = (bando.get("obiettivo_Finalita") or "").lower()
    keywords = MACROAREA_KEYWORDS[macroarea]
    score += 30 if any(k in finalita for k in keywords) else 15

    # B - Solidità Finanziaria (25)
    ebitda = indici["EBITDA Margin"] > 0.1
    utile = indici["ROE"] > 0
    debtratio = 0.5 <= indici["Debt/Equity"] <= 2
    critici = sum([not ebitda, not utile, not debtratio])
    score += max(0, 25 - critici * 8)

    # C - Forma agevolazione (15)
    forma = (bando.get("Forma_agevolazione") or "").lower()
    if "fondo perduto" in forma:
        score += 15
    elif "fiscale" in forma:
        score += 10
    else:
        score += 5

    # D - Dimensione azienda (10)
    tipo = "PMI" if azienda["dipendenti"] < 250 else "Grande"
    target = (bando.get("target") or "").lower()
    score += 10 if tipo.lower() in target else 5

    # E - Capacità co-finanziamento (10)
    if indici["EBIT/OF"] > 1 or indici["PFN/MOL"] < 6:
        score += 10
    else:
        score += 5

    # F - Territorio/ATECO (10)
    if azienda["regione"].lower() in (bando.get("regione") or "").lower():
        score += 5
    if azienda["codice_ateco"] in (bando.get("codice_ateco") or ""):
        score += 5

    return min(score, 100)

def classifica(score):
    if score >= 80:
        return "✅ Alta probabilità"
    elif score >= 50:
        return "⚠️ Media probabilità"
    else:
        return "❌ Bassa probabilità"

# === PDF e CSV report ===
def genera_csv(bandi):
    df = pd.DataFrame(bandi)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_path = "/tmp/bandi_filtrati.csv"
    with open(csv_path, "w") as f:
        f.write(csv_buffer.getvalue())
    return csv_path

def genera_pdf(bandi):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Bandi Consigliati", ln=True)
    for b in bandi:
        pdf.multi_cell(0, 8, f"{b['titolo']}\nScore: {b['score']}\n{b['valutazione']}\n---")
    pdf_path = "/tmp/bandi_filtrati.pdf"
    pdf.output(pdf_path)
    return pdf_path

# === Pipeline Gradio ===
def pipeline(pdf):
    azienda = estrai_dati(pdf)
    macroarea = assegna_macroarea(azienda)
    indici = calcola_indici(azienda)

    oggi = datetime.today().date()
    limite = oggi + timedelta(days=30)

    # Query da Supabase
    bandi_raw = supabase.table("bandi_disponibili").select("*").execute().data

    # Filtro bandi
    bandi_validi = []
    for b in bandi_raw:
        try:
            if b.get("fondo_perduto") != True:
                continue
            scad = datetime.fromisoformat(b["data_scadenza"]).date()
            if scad <= limite:
                continue
            score = valuta_bando(b, macroarea, indici, azienda)
            b["score"] = score
            b["valutazione"] = classifica(score)
            bandi_validi.append(b)
        except:
            continue

    bandi_validi.sort(key=lambda x: x["score"], reverse=True)
    csv_path = genera_csv(bandi_validi)
    pdf_path = genera_pdf(bandi_validi)

    output_testuale = "\n\n".join([f"{b['titolo']}\nScore: {b['score']}\n{b['valutazione']}" for b in bandi_validi[:10]])
    return output_testuale, csv_path, pdf_path

interface = gr.Interface(
    fn=pipeline,
    inputs=gr.File(label="Carica PDF Bilancio", file_types=[".pdf"]),
    outputs=[
        gr.Textbox(label="Top 10 Bandi Consigliati"),
        gr.File(label="Scarica CSV"),
        gr.File(label="Scarica PDF")
    ],
    title="Ricerca Bandi su Misura",
    description="Analisi bilancio → macroarea → bandi filtrati da Supabase con scoring."
)

interface.launch(server_name="0.0.0.0", server_port=8080)
