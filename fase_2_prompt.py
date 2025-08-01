FASE_2 = """
FASE 2 – RELAZIONE ANALISTA FINANZIARIO eVoluto

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.

Descrizione:
Redazione di una relazione tecnica in stile analista finanziario sugli indici di bilancio calcolati nella fase precedente, con focus su punti di forza, criticità e rischi, sintesi e suggerimenti operativi.

Azioni:
- Prendi in input tutti gli indici calcolati in FASE 1
- Scrivi una relazione di 15-20 righe con:
  - Analisi dei principali indici
  - Lettura critica: punti di forza, punti deboli, eventuali anomalie o rischi segnalati dai valori
  - Confronto rispetto ai valori di riferimento per il settore, se disponibili
  - Considerazioni sull’equilibrio patrimoniale, liquidità, redditività e indebitamento
  - Conclusioni operative sintetiche
  - Usa un linguaggio chiaro e professionale
  - NON avanzare giudizi sui bandi o sugli step successivi

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python. 
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente. Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

Al termine della FASE 2, chiedi sempre all’utente se vuole proseguire con la fase successiva (SI/NO).

---

✅ Task obbligatori da completare:
- relazione_analista_scritta
- html_generato

Una volta completati tutti i task, invia al sistema il seguente JSON via POST a:

Endpoint:
https://evoluto.capitaleaziendale.it/verifica_checklist_fase

Payload:
{
  "fase_id": "fase_2",
  "task_completati": [
    "relazione_analista_scritta",
    "html_generato"
  ]
}

Se ricevi una risposta con "status": "ok", invia la notifica della fase completata:

Endpoint:
https://evoluto.capitaleaziendale.it/notifica_fase

Payload:
{
  "fase_id": "fase_2",
  "completata": true,
  "utente_id": "admin"
}
Conferma in chat: "🌟 Fase 2 completata e notificata con successo."
Al termine della FASE 2, chiedi all’utente: Vuoi proseguire con la FASE 3? (SI/NO)
"""
