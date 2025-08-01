ISTRUZIONI_HTML = """
Alla fine trascrivi questa fase in formato HTML completo, pronto per essere salvato come file `.html` e utilizzato in un documento ufficiale.

Istruzioni:

– Genera un documento HTML valido e completo: includi i tag <html>, <head>, <meta charset="UTF-8">, <style> e <body>  

– Inserisci nel <head> uno stile CSS coerente con il design Apple moderno (glassmorphism + effetto lucido iOS):
 • Font: 'San Francisco', oppure '-apple-system', sans-serif  
 • Sfondo: sfumato grigio chiarissimo `linear-gradient(to bottom right, #f8f9fa, #e9ecef)`  
 • Testo: colore #111  
 • Tabelle con effetto lucido:
  ◦ background: rgba(255, 255, 255, 0.4)  
  ◦ border-radius: 16px  
  ◦ border: 1px solid rgba(255, 255, 255, 0.3)  
  ◦ box-shadow: 0 16px 40px rgba(0, 0, 0, 0.15)  
  ◦ backdrop-filter: blur(20px) saturate(180%)  
  ◦ background-clip: padding-box  
  ◦ overlay lucido: `::before` con gradient semi-trasparente

 • Intestazioni: `background: rgba(245,245,245,0.85)`, padding 16px  
 • Celle: padding 16px, linee divisorie sottili `border-top: 1px solid rgba(0, 0, 0, 0.05)`

– Struttura il contenuto con:
 • Titoli in <h1>, <h2>, <h3>  
 • Paragrafi in <p>  
 • Elenchi puntati in <ul><li>  
 • Tabelle in <table><tr><th><td>  

– Non usare:
 • Emoji o simboli grafici  
 • Colori accesi o layout scuri  
 • Riferimenti al numero della fase, a GPT o a messaggi meta-conversazionali  
 • Introduzioni o conclusioni fuori testo

Salva il file con il nome:
fase_[NUMERO]__[NOME-AZIENDA].html  
Sostituisci [NUMERO] con il numero reale della fase, e [NOME-AZIENDA] con il nome dell’azienda in MAIUSCOLO e trattino per spazi (es. “ACME-SRL”).

Restituisci direttamente il file `.html` completo e scaricabile, **senza mostrare codice o anteprima**.
"""
