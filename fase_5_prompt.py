fase_5 = {
    "fase_5": """
FASE 5 – SCORING E SELEZIONE DEGLI INCENTIVI

OGNI PASSAGGIO E PUNTO DELLA FASE E' OBBLIGATORIO.

Descrizione: Analisi tecnica e selezione dei 5 bandi migliori su base comparativa

La probabilità di Approvazione dei TOP 5 bandi è sempre diversa per ciascun bando perché calcolata con criteri professionali.

Azioni:
- Confronta ogni bando ricevuto con i dati aziendali
- Applica 10 criteri professionali di scoring:
  1. Spesa minima vs capacità di anticipo
  2. Tempistiche vs liquidità disponibile
  3. Forma agevolazione
  4. Solidità aziendale
  5. Obiettivo coerente
  6. Probabilità di approvazione personalizzata
  7. Dotazione residua
  8. Compatibilità dimensionale
  9. Coerenza delle spese ammissibili
  10. Requisiti impliciti
- Assegna un punteggio 0–100 con motivazione tecnica
- Seleziona i 5 bandi con punteggio più alto (≥ 80)
- Compila per ciascuno i 13 elementi vincolanti

Campi obbligatori per ogni bando:
1. Titolo del Bando  
2. Data di Scadenza  
3. Obiettivo  
4. Probabilità di Approvazione  
5. Finalità della misura  
6. Spese Ammissibili  
7. Intensità Agevolazione  
8. Importo Minimo Ammissibile  
9. Tempi medi di approvazione  
10. Dotazione Complessiva  
11. Classificazione Finale  
12. Motivazione Tecnica (5–8 righe)
13. Descrizione Dettagliata (10–12 righe)

Ogni bando deve avere una probabilità di approvazione unica, anche minima. Nessun duplicato.

NON INVENTARE MAI IL NOME DELLA FASE SUCCESSIVA  
Al termine di questa fase genera il file HTML secondo le indicazioni ricevute dal sistema Python.  
Mostra direttamente il contenuto del file HTML completo in chat, così che l'utente possa copiarlo o scaricarlo immediatamente.  
Non inviare il file completo a Python, limitati a confermare che il file è stato generato correttamente.

Al termine della FASE 5, chiedi all'utente se vuole continuare con la FASE 6.

Dopo aver generato l’HTML e completato tutti i task previsti, invia questa chiamata API:

**POST** `/verifica_checklist_fase`

```json
{
  "fase_id": "fase_5",
  "task_completati": [
    "scoring_criteri_applicato",
    "top_5_selezionati",
    "campi_13_compilati",
    "html_generato"
  ]
}
Conferma in chat: "🌟 Fase 5 completata e notificata con successo."
"""
