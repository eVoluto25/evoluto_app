import fitz  # PyMuPDF
import re
import logging

logger = logging.getLogger(__name__)

def estrai_testo_pymupdf(file_bytes: bytes) -> str:
    try:
        logger.info("🔍 Inizio pulizia PDF")

        testo_finale = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for pagina in doc:
                testo = pagina.get_text()
                testo = re.sub(r'\s+', ' ', testo)  # Rimuove spazi e a capo eccessivi
                testo = re.sub(r'[^a-zA-Z0-9€.,:%\-/\s]', '', testo)  # Rimuove simboli inutili
                testo_finale += testo + "\n"

        logger.info("✅ Pulizia PDF completata")
        return testo_finale.strip()

    except Exception as e:
        logger.error(f"❌ Errore durante la pulizia del PDF: {e}")
        raise
