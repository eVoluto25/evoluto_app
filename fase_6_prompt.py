fase_6 = {
    "fase_6": """
FASE 6 – BENCHMARK COMPARATIVO PERSONALIZZATO

OGNI PASSAGGIO E PUNTO DELLA FASE È OBBLIGATORIO.
Restituisci tutte le informazioni in formato testuale, senza utilizzare blocchi di codice (```) o formattazioni da programmatore.

Descrizione:
Confronto automatico con aziende simili per settore, dimensione e struttura finanziaria, basato su dati raccolti in forma anonima dal sistema eVoluto.

Azioni:
1. Calcola la media delle probabilità di approvazione dei 5 bandi selezionati in FASE 5.
2. Crea il seguente JSON (non mostrarlo all’utente):
{
  "ateco": "[Codice ATECO]",
  "regione": "[Regione]",
  "dimensione": "[Dimensione Aziendale]",
  "forma_giuridica": "[Forma Giuridica]",
  "fatturato": 0,
  "ebitda": 0,
  "utile_netto": 0,
  "patrimonio_netto": 0,
  "dipendenti": 0,
  "mcc_rating": "[MCC]",
  "z_score": 0,
  "obiettivo_azienda": "[Obiettivo Preferenziale]",
  "bandi_trovati": 5,
  "probabilita_media_approvazione": 0,
  "data_analisi": "[Data odierna]"
}
3. Invia il JSON all’endpoint https://evoluto.capitaleaziendale.it/analizza-azienda
4. Ricevi il messaggio di confronto e mostrane il contenuto esattamente come ricevuto, aggiungendo solamente la seguente nota dell'analista:

Nota analitica del sistema eVoluto:
- Le aziende considerate nel benchmark potrebbero presentare, in fase iniziale, situazioni di rating e scoring inferiori rispetto ai valori finali rilevati.
L’incremento osservato è stato spesso associato a interventi veloci e mirati in ambito digitale o energetico (i più veloci e semplici da attuare), risultati in diversi casi determinanti ai fini dell’approvazione.

Questo conferma che alcuni accorgimenti strategici, spesso sottovalutati o rimandati, possono oggi fare la differenza, sfruttando leve tecniche e premialità non visibili a prima lettura, con un impatto economico contenuto o nullo per l’azienda.

Integra infine un paragrafo aggiuntivo con il CONFRONTO ECONOMICO AVANZATO rispetto alle imprese dello stesso settore.

Il paragrafo deve contenere:
	1.	Stima dell’incentivo pubblico cumulabile che l’impresa può ottenere sulla base dei bandi selezionati nella FASE 5, con range minimo e massimo (es. €XX.000–€YY.000).
	2.	Confronto con i dati medi del settore (ATECO, dimensione, regione), includendo:
	•	valore medio ottenuto da imprese simili (es. €XX.000)
	•	% media di successo (es. XX%)
	•	% imprese che accedono effettivamente ai fondi (es. XX%)
	3.	Analisi del vantaggio competitivo dell’impresa analizzata (es. rating superiore alla media, bilancio in utile, profilo idoneo, maggiore probabilità di approvazione, o eventuali penalizzazioni dovute ai valori del bilancio)
	4.	Conclusione in linguaggio semplice e professionale:
	•	spiegazione pratica del significato per l’imprenditore
	•	incentivo ad attivare almeno 1 intervento per beneficiare del vantaggio competitivo già acquisito o per recuperare terreno rispetto ai competitors.

Il tono deve essere professionale ma comprensibile anche da chi non ha conoscenze finanziarie.

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

Al termine della FASE 6, chiedi all’utente: Vuoi proseguire con la FASE 7? (SI/NO)

Dopo aver generato l’HTML e completato tutti i task previsti, invia questa chiamata API:

**POST** `/verifica_checklist_fase`

```json
{
  "fase_id": "fase_6",
  "task_completati": [
    "media_probabilita_calcolata",
    "json_benchmark_inviato",
    "risultato_benchmark_ricevuto",
    "confronto_economico_avanzato_aggiunto",
    "html_generato"
  ]
}
Conferma in chat: "🌟 Fase 6 completata e notificata con successo."
Al termine della FASE 6, chiedi all’utente: Vuoi proseguire con la FASE 7? (SI/NO)
"""
