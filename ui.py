# ui.py – Interfaccia Gradio aggiornata con analisi Claude automatica su top 3 bandi

import gradio as gr
import json
from analisi_indici import estrai_dati_gpt_mock
from macroarea_logica import assegna_macroarea
from matching_bandi import filtra_bandi_macroarea
from scoring_bandi import calcola_scoring_bando
from claude_fallback import analizza_top_bandi

STATO = {
    "azienda": None,
    "indici": None,
    "macroarea": None,
    "bandi_filtrati": [],
    "bandi_scoring": [],
    "claude_output": []
}

def step_1_analizza(pdf_file):
    if not pdf_file:
        return "Nessun file caricato", None

    dati = estrai_dati_gpt_mock(pdf_file.name)
    STATO["azienda"] = dati["anagrafica"]
    STATO["indici"] = dati["bilancio"]
    macroarea = assegna_macroarea(STATO["indici"], STATO["azienda"])
    STATO["macroarea"] = macroarea

    azienda_txt = json.dumps(STATO["azienda"], indent=2, ensure_ascii=False)
    indici_txt = json.dumps(STATO["indici"], indent=2, ensure_ascii=False)
    return f"Macroarea: {macroarea}", f"Azienda:\n{azienda_txt}\n\nIndici:\n{indici_txt}"

def step_2_filtra_bandi():
    bandi = filtra_bandi_macroarea(STATO["macroarea"])
    STATO["bandi_filtrati"] = bandi
    return f"{len(bandi)} bandi compatibili trovati."

def step_3_scoring():
    risultati = []
    for bando in STATO["bandi_filtrati"]:
        score_data = calcola_scoring_bando(bando, STATO["azienda"], STATO["indici"], STATO["macroarea"])
        if score_data["score"] >= 80:
            risultati.append({
                "ID": bando["ID_Incentivo"],
                "Titolo": bando["Titolo"],
                "Score": score_data["score"],
                "Fascia": score_data["fascia"],
                "Bando": bando,
                "Scoring": score_data
            })
    STATO["bandi_scoring"] = sorted(risultati, key=lambda x: -x["Score"])
    opzioni = [f"{r['ID']} – {r['Titolo']} ({r['Score']} pt)" for r in STATO["bandi_scoring"]]
    return opzioni

def step_4_claude_batch():
    risultati = analizza_top_bandi(
        STATO["bandi_scoring"],
        STATO["azienda"],
        STATO["macroarea"],
        STATO["indici"]
    )
    STATO["claude_output"] = risultati
    return json.dumps(risultati, indent=2, ensure_ascii=False)

def esporta_risultato():
    export = {
        "azienda": STATO["azienda"],
        "indici": STATO["indici"],
        "macroarea": STATO["macroarea"],
        "bandi": STATO["bandi_scoring"],
        "claude": STATO["claude_output"]
    }
    with open("/mnt/data/risultato_evoluto.json", "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2, ensure_ascii=False)
    return "/mnt/data/risultato_evoluto.json"

with gr.Blocks(title="eVoluto – Analisi PDF + Matching Bandi") as demo:
    gr.Markdown("# 📊 Sistema eVoluto – Matching Bandi Finanza Agevolata")

    with gr.Row():
        pdf_input = gr.File(label="📁 Carica il Bilancio PDF")
        btn_analizza = gr.Button("1️⃣ Analizza Bilancio")
    out_macro, out_dati = gr.Textbox(label="Macroarea", lines=1), gr.Textbox(label="Dati estratti", lines=10)

    btn_match = gr.Button("2️⃣ Filtra Bandi")
    out_match = gr.Textbox(label="Risultati Matching")

    btn_scoring = gr.Button("3️⃣ Calcola Scoring")
    bandi_lista = gr.Dropdown(choices=[], label="Bandi con Score ≥ 80")

    btn_claude = gr.Button("4️⃣ Analisi Claude (Top 3)")
    out_claude = gr.Textbox(label="Risposte Claude", lines=10)

    btn_export = gr.Button("📤 Esporta JSON")
    out_file = gr.File(label="Download Risultati")

    btn_analizza.click(step_1_analizza, inputs=pdf_input, outputs=[out_macro, out_dati])
    btn_match.click(step_2_filtra_bandi, outputs=out_match)
    btn_scoring.click(step_3_scoring, outputs=bandi_lista)
    btn_claude.click(step_4_claude_batch, outputs=out_claude)
    btn_export.click(esporta_risultato, outputs=out_file)

demo.launch()