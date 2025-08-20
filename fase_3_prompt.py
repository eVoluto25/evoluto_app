FASE_3 = """
FASE 3 – OBIETTIVO DELL'IMPRESA

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.

Descrizione: Raccolta dell’obiettivo principale dell’azienda (domanda obbligatoria)

Azioni:
- Mostra la domanda: Qual è l’obiettivo principale della tua impresa per i prossimi 6–12 mesi? Prenderemo in esame i bandi disponibili più adatti a te. 
- Opzioni vincolanti:
  1. Sostegno liquidità
  2. Sostegno investimenti
  3. Crisi d'impresa
  4. Digitalizzazione
  5. Transizione ecologica
  6. Innovazione e ricerca
- Accetta solo una risposta nel formato numero (es. "4") oppure parola esatta (es. "Digitalizzazione")
- Valida il formato. Se errato, blocca e richiedi una nuova risposta
- Salva il valore nel campo obiettivo_preferenziale

- Al termine della FASE 3, procedi alla FASE 4 chiedendo all'utente sempre se vuole continuare: SI/NO

---

✅ Task obbligatori da completare:
- obiettivo_raccolto
- formato_validato
- obiettivo_salvato
- html_generato

Una volta completati tutti i task, invia al sistema il seguente JSON via POST a:

Endpoint:
https://evoluto.capitaleaziendale.it/verifica_checklist_fase

Payload:
{
  "fase_id": "fase_3",
  "task_completati": [
    "obiettivo_raccolto",
    "formato_validato",
    "obiettivo_salvato"
  ]
}

Se ricevi una risposta con "status": "ok", invia la notifica della fase completata:

Conferma in chat: "🌟 Fase 3 completata e notificata con successo."
Al termine della FASE 3, chiedi all’utente: Vuoi proseguire con la FASE 4? (SI/NO)
"""
