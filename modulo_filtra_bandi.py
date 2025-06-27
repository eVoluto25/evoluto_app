modulo_filtrato_clean = '''
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def filtra_bandi(df, codice_ateco=None, regione=None, dimensione=None, forma_agevolazione=None, max_results=5):
    logger.info("🔍 Entrata nella funzione filtra_bandi")

    # Normalizza nomi colonne
    df.columns = [col.lower() for col in df.columns]
    logger.info(f"📊 DataFrame iniziale: {len(df)} righe")

    # Usa solo colonne pulite
    if 'codici_ateco_clean' in df.columns:
        df['codici_ateco'] = df['codici_ateco_clean']
    if 'regioni_clean' in df.columns:
        df['regioni'] = df['regioni_clean']
    if 'dimensioni_clean' in df.columns:
        df['dimensioni'] = df['dimensioni_clean']
    if 'forma_agevolazione_clean' in df.columns:
        df['forma_agevolazione'] = df['forma_agevolazione_clean']

    # Filtro codice ATECO
    if codice_ateco:
        def match_codice_ateco(lista):
            if isinstance(lista, list) and len(lista) > 0:
                if "tutti" in [x.strip().lower() for x in lista]:
                    return True
                return any(str(codice_ateco).startswith(str(c).strip()) for c in lista)
            return False
        df = df[df["codici_ateco"].apply(match_codice_ateco)]
        logger.info(f"✅ Filtro codice ATECO: {codice_ateco}")

    # Filtro regione
    if regione:
        df = df[df["regioni"].apply(lambda x: regione in x if isinstance(x, list) else False)]
        logger.info(f"🌍 Filtro regione: {regione}")

    # Filtro dimensione
    if dimensione:
        df = df[df["dimensioni"].apply(lambda x: dimensione in x if isinstance(x, list) else False)]
        logger.info(f"🏢 Filtro dimensione: {dimensione}")

    # Filtro forma agevolazione
    if forma_agevolazione:
        df = df[df["forma_agevolazione"].apply(lambda x: forma_agevolazione in x if isinstance(x, list) else False)]
        logger.info(f"💶 Filtro forma agevolazione: {forma_agevolazione}")

    # Restituisci solo i primi N risultati
    risultati = df.head(max_results)
    logger.info(f"🎯 Filtro bandi completato: {len(risultati)} bandi trovati")
    return risultati
'''

# Salvo il file aggiornato
clean_file_path = "/mnt/data/modulo_filtra_bandi_clean.py"
with open(clean_file_path, "w", encoding="utf-8") as f:
    f.write(modulo_filtrato_clean)

clean_file_path
