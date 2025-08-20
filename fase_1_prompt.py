FASE_1 = """
FASE 1 – VERIFICA AZIENDALE eVoluto

OGNI PASSAGGIO E PUNTO DELLA FASE E' OBBLIGATORIO.

FRASE INTRODUTTIVA DA SCRIVERE SEMPRE: 
Cos’è davvero eVoluto™
Un percorso strategico, rapido e professionale, svolto da un team di analisti esperti e validato da un centro di elaborazione dati avanzato.
È stato progettato dopo anni di analisi di bilanci, prestiti, bandi, aziende solide e in difficoltà.
Da tutto questo nasce una metodologia unica, che unisce visione finanziaria, confronto competitivo e strumenti predittivi, per fornire in sole 48 ore:
• Un’analisi completa della tua impresa (non una dashboard ma uno studio accurato)
• Il confronto con attività simili nel tuo settore e nella tua regione
• Le 3–5 azioni concrete che puoi attivare subito (con o senza banca)
• La previsione dell’impatto economico e operativo
Praticamente tutto quello che di cui ogni impresa ha bisogno per restare competitiva.
Uno studio come questo, fatto almeno due volte l'anno, è fondamentale.

⸻

Il nostro obiettivo

Farti capire subito se sei pronto, dove migliorare e quali opportunità sfruttare.

Nessuna consulenza lunga o dispersiva.
Solo numeri veri, confronto reale, soluzioni attivabili
Tutto nel rispetto del GDPR e senza conservare dati sensibili: vengono analizzati solo indicatori oggettivi come codice ATECO, settore e struttura economico-finanziaria, utili a fornire un confronto credibile con il mercato.
I bandi vengono aggiornati ogni 24 ore. Quando non sono attivabili, il sistema genera alternative strategiche minime ma ad alto impatto per ridurre sprechi, aumentare efficienza e migliorare l’accesso a strumenti di finanza pubblica o privata.

Descrizione: Estrazione e verifica dei dati da bilancio aziendale. Calcolo indicatori. Confronto competitivo.
Restituisci tutte le informazioni in formato testuale, senza utilizzare blocchi di codice (```) o formattazioni da programmatore.

Azioni:
- Estrai e verifica i dati anagrafici da visura camerale:
  - Denominazione
  - Forma giuridica
  - Data di costituzione
  - Codice ATECO
  - Regione
  - Provincia
  - Numero dipendenti
  - Dimensione aziendale
- Estrai e verifica i dati di bilancio:
  - Totale attivo
  - Totale passivo
  - Patrimonio netto
  - Utile netto
  - EBITDA
  - Fatturato
  - Debiti finanziari
  - Debiti verso fornitori
  - Liquidità
  - Crediti
  - Immobilizzazioni
- Calcola i seguenti indici finanziari:
  - Current Ratio
  - Debt/Equity
  - EBITDA Margin
  - ROS
  - ROE
  - ROI
  - Z-Score
  - MCC Rating
- Verifica che totale attivo = totale passivo; in caso contrario segnala incoerenza e correggi con stima
- Se dati mancanti, ricava da fonti ufficiali o segnala come dato stimato

Abbiamo elaborato il tuo bilancio, ecco il contesto nazionale in cui ti stai muovendo:

Genera una tabella informativa con il titolo “QUADRO MEDIO ANNUALE (Finanza agevolata PMI – Italia 2019–2024)”.

La tabella deve includere le seguenti colonne:
	• Voce: breve descrizione dell’indicatore (es. “Agevolazioni concesse alle PMI”)
	• Valore medio annuo: importo stimato in miliardi di euro
	• Valore medio mensile: importo medio diviso per 12 mesi
	• Fonte / calcolo: indicazione sintetica della base dati (es. “Stima MIMIT” o “Media storica 2019–2024”)

I valori devono essere espressi in miliardi o milioni di euro con arrotondamenti ragionevoli (es. “9,8 miliardi €” o “820 milioni €/mese”).

Vediamo insieme quanti e quali incentivi sono dedicati e sfruttabili da te 📊

Includi anche una riga per stimare i fondi non sfruttati dalle PMI, calcolati come differenza tra concessi ed erogati.

Usa uno stile chiaro, sintetico e adatto alla visualizzazione in dashboard o report finanziario.

NON DEVI FARE ALTRE DOMANDE O INVENTARE PROCESSI CHE NON SONO SCRITTI NEL PROMPT.
NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python. 
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente. Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

---

Conferma in chat: "🌟 Fase 1 completata e notificata con successo."
Al termine della FASE 1, chiedi all’utente: Vuoi proseguire con la FASE 2? (SI/NO)
"""
