from pydantic import BaseModel
from typing import Optional

class Anagrafica(BaseModel):
    codice_ateco: Optional[str] = None
    regione: Optional[str] = None
    forma_giuridica: Optional[str] = None
    numero_dipendenti: Optional[int] = None
    attivita_prevalente: Optional[str] = None

class Bilancio(BaseModel):
    ricavi: Optional[float] = 0
    utile_netto: Optional[float] = 0
    ebitda: Optional[float] = 0
    totale_attivo: Optional[float] = 0
    immobilizzazioni: Optional[float] = 0
    ricavi_anno_prec: Optional[float] = None

class RisposteTest(BaseModel):
    crisi_impresa: Optional[str] = None
    sostegno_liquidita: Optional[str] = None
    sostegno_investimenti: Optional[str] = None
    transizione_ecologica: Optional[str] = None
    innovazione_ricerca: Optional[str] = None

class InputDati(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio
    risposte_test: RisposteTest
