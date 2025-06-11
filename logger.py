# logger.py
import logging

logger = logging.getLogger("analisi_bandi")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("/tmp/analisi_bandi.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)
