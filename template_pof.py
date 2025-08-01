### Template HTML per la generazione della fase finale in stile Apple moderno


ISTRUZIONI_HTML = """ 
Alla fine trascrivi questa fase in formato HTML completo, pronto per essere salvato come file `.html` e utilizzato in un documento ufficiale.

Istruzioni:

– Genera un documento HTML valido e completo: includi i tag <html>, <head>, <meta charset="UTF-8">, <style> e <body>  

– Inserisci nel <head> uno stile CSS coerente con il design Apple moderno (glassmorphism potenziato con riflesso e rilievo):

 • Font: 'Montaser Arabic', sans-serif  
 • Sfondo: sfumato grigio chiaro con accenno di azzurro (#f8f9fa → #e3f2fd)  
 • Testo: colore #111  
 • Titolo principale <h1>: colore grigio scuro #444  
 • Cornici (blocchi <div>): effetto vetro traslucido con bordo arrotondato, ombra diffusa, sfondo azzurrato semi-trasparente (`rgba(230,245,255,0.25)`), animazione `fadeIn`, filtro `blur(25px)`  
 • Tabelle: sfondo vetroso, intestazioni con colore chiaro, celle con padding minimo 16px, righe con linee divisorie leggere (`1px solid rgba(0,0,0,0.08)`)  
 • Paragrafi: ogni <p> va inserito in una "card" con bordo inferiore leggero (`1px solid rgba(0,0,0,0.05)`)  
 • Layout: elegante, leggibile, effetto iOS

– Struttura il contenuto con:
 • Titoli in <h1>, <h2>, <h3>  
 • Paragrafi chiari in <p>  
 • Elenchi puntati in <ul><li>  
 • Tabelle complete in <table><tr><th><td>, con intestazioni ben evidenziate e colonne separate visivamente  

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
