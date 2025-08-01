master_flow["fase_8"] = """
FASE 8 – SCENARI PREDITTIVI: TRA ANALISI, STRUTTURA AZIENDALE E PREVISIONI DELL'INTELLIGENZA ARTIFICIALE

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.

“In base ai dati e all’analisi effettuata, quali sono 3 scenari predittivi (ottimistico, realistico, conservativo) sull’evoluzione economica dell'azienda analizzata nei prossimi 12 mesi se accede al primo bando selezionato? Includi rischi principali, leva finanziaria potenziale e impatto atteso su margini, investimenti e posizione competitiva.”

Aggiungiamo queste 3 richieste finali:

Descrivi in massimo 3 bullet:
	•	i punti di debolezza aziendale
	•	le priorità economiche da sistemare
	•	i motivi per cui serve agire subito

Indica anche esplicitamente cosa NON è utile attivare oggi, se presente tra le soluzioni standard.

🟢 Mostra almeno 1 bando prioritario effettivamente compatibile diverso da quello dell'esempio nello scenario predittivo: più semplice e meno costoso, con breve motivazione tecnica.

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

✅ Invio dei task completati:

Al termine, invia questa chiamata API:

POST /verifica_checklist_fase

{
  "fase_id": "fase_8",
  "task_completati": [
    "scenari_predittivi_generati",
    "analisi_debolezze_priorita_motivi_compilata",
    "soluzioni_non_utili_evidenziate",
    "bando_alternativo_prioritario_individuato",
    "html_generato"
  ]
}

Se ricevi "status": "ok" allora invia:

POST /notifica_fase

{
  "fase_id": "fase_8",
  "status": "ok"
}

Conferma in chat: "🌟 Fase 8 completata e notificata con successo."
Al termine della FASE 8, chiedi all’utente: Vuoi proseguire con la FASE 9? (SI/NO)
"""
