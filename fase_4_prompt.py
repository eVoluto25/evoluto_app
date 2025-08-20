FASE_4 = """
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

Conferma in chat: "🌟 Fase 4 completata e notificata con successo."
Al termine della FASE 4, chiedi all’utente: Vuoi proseguire con la FASE 5? (SI/NO)
"""
