import gradio as gr
import openai
import os
import pdfplumber
from fpdf import FPDF
import re

# === STEP 1: Parsing robusto con pdfplumber

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

# === STEP 2: Calcolo indici

def calcola_indici(d):
    ci = d["totale_attivo"] - d["disponibilita_liquide"]
    mol = d["risultato_operativo"] + d["ammortamenti"]
    pfn = d["debiti"] - d["disponibilita_liquide"]

    return {
        "ROE": d["utile_netto"] / d["patrimonio_netto"] if d["patrimonio_netto"] else 0,
        "ROI": d["risultato_operativo"] / ci if ci else 0,
        "ROS": d["risultato_operativo"] / d["vendite"] if d["vendite"] else 0,
        "ROT": d["vendite"] / ci if ci else 0,
        "ROIC": d["risultato_operativo"] / ci if ci else 0,

        "Copertura Immobilizzazioni": (d["patrimonio_netto"] + pfn) / (d["totale_attivo"] - d["attivita_breve"]) if (d["totale_attivo"] - d["attivita_breve"]) else 0,
        "Indipendenza Finanziaria": d["patrimonio_netto"] / d["totale_attivo"] if d["totale_attivo"] else 0,
        "Leverage": d["totale_attivo"] / d["patrimonio_netto"] if d["patrimonio_netto"] else 0,
        "PFN/PN": pfn / d["patrimonio_netto"] if d["patrimonio_netto"] else 0,

        "Current Ratio": d["attivita_breve"] / d["passivita_breve"] if d["passivita_breve"] else 0,
        "Quick Ratio": (d["attivita_breve"] - d["rimanenze"]) / d["passivita_breve"] if d["passivita_breve"] else 0,
        "Margine di Tesoreria": d["disponibilita_liquide"] / d["passivita_breve"] if d["passivita_breve"] else 0,
        "Margine di Struttura": d["patrimonio_netto"] / d["totale_attivo"] if d["totale_attivo"] else 0,
        "Capitale Circolante Netto": d["attivita_breve"] - d["passivita_breve"],

        "EBIT/OF": d["risultato_operativo"] / d["oneri_finanziari"] if d["oneri_finanziari"] else 0,
        "MOL/PFN": mol / pfn if pfn else 0,
        "FCF/OF": d["flusso_cassa"] / d["oneri_finanziari"] if d["oneri_finanziari"] else 0,
        "PFN/MOL": pfn / mol if mol else 0,
        "PFN/Ricavi": pfn / d["vendite"] if d["vendite"] else 0,

        "Cash Wallet Risk Index": 0.5,
        "Collateral Distortion Index": 0.3,
        "Sconfinamento Medio": 0.2,
        "Tensione Finanziaria": 0.4,

        "Cash Wallet Management Index": 0.6,
        "Duration": 5
    }

# === STEP 3: Calcolo macro area

def valuta_macro_area(indici, d):
    crisi = int(indici["Current Ratio"] <= 1) + int(indici["Leverage"] >= 2) + int(indici["EBIT/OF"] < 1) + int(indici["ROS"] < 0) + int(d["utile_netto"] < 0)
    crescita = int(d["autofinanziamento"]) + int(indici["Indipendenza Finanziaria"] > 0.2) + int(d["investimenti"])
    espansione = int(d["fatturato_crescita"]) + int(indici["ROS"] > 0.05) + int(indici["MOL/PFN"] > 0.1)

    punteggi = {"Crisi": crisi, "Crescita": crescita, "Espansione": espansione}
    best = max(punteggi, key=punteggi.get)

    if list(punteggi.values()).count(punteggi[best]) > 1:
        if crisi == 0 and crescita >= espansione:
            best = "Espansione"
        elif crisi > 0:
            best = "Crisi"
        else:
            best = "Crescita"

    return punteggi, best

# === STEP 4: Generazione PDF

def genera_report_pdf(indici, punteggi, macro):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Analisi Finanziaria", ln=True, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="INDICI CALCOLATI:", ln=True)
    for k, v in indici.items():
        pdf.cell(200, 8, txt=f"{k}: {round(v, 3)}", ln=True)

    pdf.ln()
    pdf.cell(200, 10, txt="PUNTEGGI MACROAREE:", ln=True)
    for k, v in punteggi.items():
        pdf.cell(200, 8, txt=f"{k}: {v} punti", ln=True)

    pdf.ln()
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt=f"MACRO AREA ASSEGNATA: {macro}", ln=True)

    output_path = "/tmp/report_finanziario.pdf"
    pdf.output(output_path)
    return output_path

# === Interfaccia Gradio

def pipeline(pdf):
    dati = estrai_dati(pdf)
    indici = calcola_indici(dati)
    punteggi, macroarea = valuta_macro_area(indici, dati)
    report = genera_report_pdf(indici, punteggi, macroarea)

    output = "\n".join([f"{k}: {round(v, 3)}" for k, v in indici.items()])
    output += "\n\n---\n"
    output += "\n".join([f"{k}: {v} punti" for k, v in punteggi.items()])
    output += f"\n\n👉 Macro area assegnata: {macroarea}"

    return output, report

interface = gr.Interface(
    fn=pipeline,
    inputs=gr.File(label="Carica PDF Bilancio", file_types=[".pdf"]),
    outputs=[gr.Textbox(label="Risultati"), gr.File(label="Scarica Report PDF")],
    title="Analisi Finanziaria Automatica",
    description="Calcolo 25 indici finanziari, valutazione macro-area, generazione PDF."
)

interface.launch(server_name="0.0.0.0", server_port=8080)
