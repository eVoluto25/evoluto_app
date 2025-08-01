master_flow["fase_10"] = """
FASE 10 – VERIFICA DI ALLINEAMENTO TECNICO-FINANZIARIO 

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.
Restituisci tutte le informazioni in formato testuale, senza blocchi codice o linguaggi da programmatore.

🎯 Obiettivo della fase

Questa fase serve a valutare bene e con attenzione se e quanto l’impresa è pronta per realizzare gli interventi premianti suggeriti nella FASE 8, verificando:
	•	la compatibilità tecnica con la struttura attuale dell’impresa
	•	la rilevanza per il settore di appartenenza
	•	la sostenibilità economica e finanziaria degli investimenti

L’obiettivo è fornire una guida chiara e concreta su cosa attivare, in che ordine, e con quali formule economiche realmente accessibili.

⸻

⚙️ Azioni:
1. Recupera i seguenti dati aziendali dalle fasi precedenti:
	•	Codice ATECO
	•	Regione
	•	Dimensione aziendale
	•	Forma giuridica
	•	Dipendenti, Fatturato, EBITDA, Patrimonio Netto
	•	Z-Score e MCC Rating
	•	Obiettivo preferenziale scelto
	•	Eventuali criticità (es. leva finanziaria elevata, liquidità bassa)

2. Analizza i 5 ambiti premianti della FASE 8:
	•	Cybersecurity
	•	Connettività stabile
	•	Intelligenza Artificiale
	•	Efficienza energetica
	•	Tracciamento ESG e sostenibilità

3. Per ciascun ambito, compila la Tabella tecnica di allineamento con questi elementi:

Ambito | Coerenza con la struttura aziendale | Rilevanza per il settore | Rischio in fase di bando | Beneficio atteso | Priorità di intervento  
-------|--------------------------------------|--------------------------|--------------------------|-------------------|------------------------
       | ✅ Elevata / ⚠️ Parziale / ⛔ Bassa  | 🔹 Essenziale / 🔸 Utile / ⚪ Marginale | sì/no | testo sintetico | Alta / Media / Bassa  

Motiva ogni voce in linguaggio semplice, comprensibile anche per utenti non tecnici.

4. Verifica la sostenibilità finanziaria degli interventi:
	•	Analizza i dati finanziari e valuta se l’azienda ha la solidità per accedere a un finanziamento bancario.
	•	Se presenti criticità, suggerisci soluzioni alternative come:
		- Noleggio operativo
		- Leasing strumentale
		- Finanziamenti bancari o fintech
		- ESCo
		- Pagamento ricorrente (SaaS)

5. Compila la Tabella economico-finanziaria:

Ambito | Modalità consigliata | Formula utilizzata | Durata | Rata o canone stimato  
-------|----------------------|--------------------|--------|------------------------

Motiva la scelta (es. “evita esposizione bancaria”, “rateizzazione accessibile”...).

6. Esegui almeno 3 o 4 simulazioni economico-finanziarie:

	•	Importo stimato
	•	Modalità (leasing, noleggio, finanziamento)
	•	Durata in mesi
	•	Tasso ipotizzato
	•	Importo rata o canone

ℹ️ Nota sulle simulazioni finanziarie:
Le simulazioni di pagamento sono basate sui Tassi Effettivi Globali Medi (TEGM) pubblicati trimestralmente dalla Banca d’Italia.
I valori sono indicativi e non vincolanti, e non includono scontistiche o condizioni personalizzate eventualmente offerte da istituti bancari o partner tecnici.
Le condizioni effettive saranno soggette a verifica caso per caso.

📌 Verifica anche queste 3 condizioni strategiche:

❓ Hai trovato un bando ma non puoi anticipare la spesa?
💬 Soluzioni:
- Finanziamento ponte con garanzia MCC
- Anticipo su fattura (invoice trading)
- Noleggio, SaaS o leasing
- Fideiussione tecnica

❓ Hai utile netto negativo ma vuoi investire?
💬 Soluzioni:
- Canone rateizzato e rendicontabile
- Contributo pubblico cumulabile
- Intervento certificato e pre-approvabile

❓ Vuoi migliorare l’impresa senza usare banche?
💬 Soluzioni:
- SaaS (cybersecurity, dati, backup…)
- ESCo o noleggio per impianti energetici
- Voucher digitali e bandi cumulabili

7. Concludi con un commento tecnico di sintesi (18–20 righe):
	•	Spiega l’ordine degli interventi consigliati
	•	Indica eventuali combinazioni utili

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

✅ Invio dei task completati:

POST /verifica_checklist_fase

{
  "fase_id": "fase_10",
  "task_completati": [
    "recupero_dati_azienda",
    "analisi_ambiti_premianti",
    "tabella_allineamento_tecnico",
    "valutazione_sostenibilità",
    "simulazioni_finanziarie",
    "tabella_economica",
    "commento_tecnico_finale",
    "html_generato"
  ]
}

Se ricevi "status": "ok" allora invia:

POST /notifica_fase

{
  "fase_id": "fase_10",
  "status": "ok"
}

Al termine della FASE 10, chiedi all'utente se vuole continuare con la FASE 11.
"""
