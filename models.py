from pydantic import BaseModel

class AziendaInput(BaseModel):
    dimensione: str  # Esempio: "Microimpresa", "Piccola Impresa", ecc.
    regione: str     # Esempio: "Lombardia", "Lazio", ecc.
    obiettivo_preferenziale: str  # Esempio: "Innovazione", "Sostegno", ecc.
    mcc_rating: str  # Esempio: "BBB", "AA", ecc.
    z_score: float   # Esempio: -1.2, 0.5, ecc.
