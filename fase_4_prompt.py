prompt_fase_4 = """
FASE 4 – MATCHING INTELLIGENTE eVoluto

OGNI PASSAGGIO E PUNTO DELLA FASE E' OBBLIGATORIO.
Restituisci tutte le informazioni in formato testuale, senza utilizzare blocchi di codice (```) o formattazioni da programmatore.

Descrizione: Creazione del JSON finale e invio all’endpoint Python

Azioni:
- Crea il seguente JSON (non mostrarlo mai):
  {
    "dimensione": "[Dimensione Aziendale]",
    "regione": "[Regione]",
    "obiettivo_preferenziale": "[Obiettivo Preferenziale]",
    "mcc_rating": "[MCC Rating]",
    "z_score": 0,
    "numero_dipendenti": 0,
    "ebitda": 0,
    "utile_netto": 0,
    "fatturato": 0
  }
- Invia il JSON all’endpoint /filtra-bandi
- Ricevi fino a 20 bandi compatibili
- Verifica che ogni bando contenga i dati minimi richiesti

Avvisa sempre che il sistema eVoluto ha intercettato (scrivi il numero dei bandi) idonei e adatti alle caratteristiche aziendali.

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python. 
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente. Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

Al termine della FASE 4, procedi alla FASE 5 chiedendo all'utente sempre se vuole continuare: SI/NO.

---

✅ Task obbligatori da completare:
- json_creato_e_inviato
- bandi_ricevuti
- verifica_minimi_ok
- html_generato

Una volta completati tutti i task, invia al sistema il seguente JSON via POST a:

Endpoint:
https://evoluto.capitaleaziendale.it/verifica_checklist_fase

Payload:
{
  "fase_id": "fase_4",
  "task_completati": [
    "json_creato_e_inviato",
    "bandi_ricevuti",
    "verifica_minimi_ok",
    "html_generato"
  ]
}

Se ricevi una risposta con "status": "ok", invia la notifica della fase completata:

Endpoint:
https://evoluto.capitaleaziendale.it/notifica_fase

Payload:
{
  "fase_id": "fase_4",
  "completata": true,
  "utente_id": "admin"
}

Conferma in chat: "🌟 Fase 4 completata e notificata con successo."
Al termine della FASE 4, chiedi all’utente: Vuoi proseguire con la FASE 5? (SI/NO)
"""
