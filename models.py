from pydantic import BaseModel
from typing import Optional, List

class Anagrafica(BaseModel):
    codice_ateco: Optional[str] = None
    regione: Optional[str] = None
    forma_giuridica: Optional[str] = None
    numero_dipendenti: Optional[int] = None
    attività_prevalente: Optional[str] = None

class Bilancio(BaseModel):
    ricavi: Optional[float] = 0
    utile_netto: Optional[float] = 0
    ebitda: Optional[float] = 0
    totale_attivo: Optional[float] = 0
    immobilizzazioni: Optional[float] = 0
    ricavi_anno_prec: Optional[float] = 0

class RisposteTest(BaseModel):
    risposte: List[str]  # Es: ["A", "B", "C", "A", "E", "D", "B", "C", "A", "B"]

class InputDati(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio
    risposte_test: RisposteTest
