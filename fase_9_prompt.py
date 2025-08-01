FASE_9 = """
FASE 9 – INNOVATION CHECK (VERIFICA DI ADEGUAMENTO STRATEGICO)

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.
Restituisci tutte le informazioni in formato testuale, senza utilizzare blocchi di codice (```) o formattazioni da programmatore.

Hai già adottato misure di risparmio e ottimizzazione?  
Queste sono le **prime ad essere valutate** nei bandi più selettivi e con un'alta percentuale di fondo perduto.
Le aziende che si sono già mosse su questi fronti ottengono **premialità dirette** e un posizionamento migliore in fase di selezione: sono sempre le prime ad accedere ai bandi più interessanti.

Verifica ora, con il nostro Innovation Manager, se la tua azienda ha già attivato:

- 🔐 **Misure di sicurezza informatica (Cybersecurity)**
- 🌐 **Connettività professionale e stabile**
- 🤖 **Automazione dei processi aziendali con l’ausilio dell’IA**
- ⚡ **Riduzione dei consumi e ottimizzazione energetica**
- 📊 **Tracciamento di indicatori ESG e sostenibilità**

Le aziende che integrano tempestivamente queste misure ottengono benefici documentati in termini di efficienza economica, punteggio tecnico e affidabilità percepita.

Segue un confronto oggettivo tra aziende adeguate e aziende non allineate:

⸻

Accessibilità ai bandi:
	•	Azienda adeguata: accesso facilitato ai bandi più selettivi con fondo perduto superiore al 50%
	•	Azienda non adeguata: rischio esclusione o ammissione con punteggio minimo

Punteggio in fase di selezione:
	•	Azienda adeguata: +20/30 punti premiali su criteri ESG, innovazione e digitalizzazione
	•	Azienda non adeguata: penalizzazione su innovazione, sostenibilità e struttura operativa

Efficienza operativa:
	•	Azienda adeguata: riduzione dei costi tra il 10% e il 18% entro 12 mesi
	•	Azienda non adeguata: costi fissi elevati, assenza di ottimizzazione interna

Rating percepito da stakeholder:
	•	Azienda adeguata: profilo stabile e tracciabile, governance attiva
	•	Azienda non adeguata: profilo debole, valutazione difficile, percezione di rischio

Posizionamento competitivo:
	•	Azienda adeguata: struttura pronta per scalabilità e attrattiva sul mercato
	•	Azienda non adeguata: difficoltà a competere con aziende già allineate

Compliance normativa:
	•	Azienda adeguata: già conforme a standard di rendicontazione e controllo
	•	Azienda non adeguata: soggetta a ritardi, sanzioni, mancato accesso a misure future

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

✅ Invio dei task completati:

Al termine, invia questa chiamata API:

POST /verifica_checklist_fase

{
  "fase_id": "fase_9",
  "task_completati": [
    "verifica_misure_attivate",
    "confronto_aziende_adeguate_vs_non",
    "valutazione_impatto_bandi",
    "html_generato"
  ]
}

Se ricevi "status": "ok" allora invia:

POST /notifica_fase

{
  "fase_id": "fase_9",
  "status": "ok"
}
Conferma in chat: "🌟 Fase 9 completata e notificata con successo."
Al termine della FASE 9, chiedi all’utente: Vuoi proseguire con la FASE 10? (SI/NO)
"""
