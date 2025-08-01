FASE_7 = """
FASE 7 – CONTI IN TASCA: CONFRONTO 360°

Istruzioni:

Analizza i costi aziendali presenti nel bilancio.
Per ogni voce significativa, confronta con la media delle aziende simili:
- stesso settore ATECO
- stessa dimensione (micro, piccola, media, grande impresa)
- stessa regione

Per ogni confronto evidenzia:
- Dove l’azienda spende troppo
- Dove è in linea
- Dove mancano voci strategiche (es. formazione, strumenti, digitalizzazione)
- Dove è migliore rispetto alla media (ottimizzazioni già fatte)

Struttura della risposta (obbligatoria):

1. Tabella confronto costi principali:

Voce di costo | Tua azienda | Media aziende simili | Differenza | Valutazione
--------------|-------------|-----------------------|------------|--------------
...           | €           | €                     | ± €        | Spendi troppo / In linea / Ottimizzato

2. Voci mancanti nel bilancio:
Elenca le voci importanti non presenti nei costi dell’azienda ma presenti in quelle simili.

3. Punti di forza rispetto ai competitor:
Evidenzia cosa l’azienda fa meglio rispetto alla media.

4. Riepilogo economico finale:
- Totale spesa in eccesso stimata
- Risparmio potenziale attivabile in 12 mesi
- Aree da correggere
- Aree dove è già competitiva
- Aree da attivare

Indicazioni di stile:
- Linguaggio semplice e diretto, nessun tecnicismo
- Non usare termini come “benchmark”, “rating”, “score”
- Niente frasi generiche, solo confronto reale con numeri chiari

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

✅ Invio dei task completati:

Al termine, invia questa chiamata API:

POST /verifica_checklist_fase

{
  "fase_id": "fase_7",
  "task_completati": [
    "tabella_confronto_costi_generata",
    "voci_mancanti_identificate",
    "punti_forza_rispetto_media_individuati",
    "riepilogo_economico_compilato",
    "html_generato"
  ]
}

Se ricevi "status": "ok" allora invia:

POST /notifica_fase

{
  "fase_id": "fase_7",
  "status": "ok"
}

Conferma in chat: "🌟 Fase 7 completata e notificata con successo."
Al termine della FASE 7, chiedi all’utente: Vuoi proseguire con la FASE 8? (SI/NO)
"""
