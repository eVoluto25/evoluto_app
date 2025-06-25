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
    ai: Optional[str]
    cybersecurity: Optional[str]
    sostenibilità: Optional[str]
    efficientamento_energetico: Optional[str]
    internazionalizzazione: Optional[str]
    innovazione: Optional[str]
    crisi: Optional[str]
    inclusione: Optional[str]
    liquidità: Optional[str]
    fisco: Optional[str]

class InputDati(BaseModel):
    anagrafica: Anagrafica
    bilancio: Bilancio
    risposte_test: RisposteTest
