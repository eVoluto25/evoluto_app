ISTRUZIONI_HTML = """
Alla fine trascrivi questa fase in formato HTML completo, pronto per essere salvato come file `.html` e utilizzato in un documento ufficiale.

Istruzioni:

– Genera un documento HTML valido e completo: includi i tag <html>, <head>, <meta charset="UTF-8">, <style> e <body>  

– Inserisci nel <head> uno stile CSS coerente con il design Apple moderno (glassmorphism):
 • Font: 'San Francisco', oppure '-apple-system', sans-serif  
 • Sfondo: sfumato color grigio chiarissimo (#f8f9fa → #e9ecef)  
 • Testo: colore #111  
 • Tabelle: sfondo bianco semi-trasparente (`rgba(255,255,255,0.6)`), **bordi arrotondati**, **bordo esterno più marcato** (`1px solid rgba(0, 0, 0, 0.1)`)  
 • Effetto rilievo: usa `box-shadow` ampio e `backdrop-filter: blur(20px)`  
 • Intestazioni grigio tenue (`rgba(245,245,245,0.85)`), celle con padding di almeno 16px, linee divisorie leggere  

– Struttura il contenuto con:
 • Titoli in <h1>, <h2>, <h3>  
 • Paragrafi chiari in <p>  
 • Elenchi puntati in <ul><li>  
 • Tabelle complete in <table><tr><th><td>, con intestazioni ben evidenziate  

– Non usare:
 • Emoji o simboli grafici  
 • Colori accesi o layout scuri  
 • Riferimenti al numero della fase, a GPT o a messaggi meta-conversazionali  
 • Introduzioni o conclusioni aggiuntive fuori testo

Salva il file con il nome:
fase_[NUMERO]__[NOME-AZIENDA].html  
Sostituisci [NUMERO] con il numero reale della fase, e [NOME-AZIENDA] con il nome dell’azienda in MAIUSCOLO e trattino per spazi (es. “ACME-SRL”).

Restituisci direttamente il file `.html` completo e scaricabile, **senza mostrare codice o anteprima**.
"""
