from models import Bilancio, Anagrafica, RisposteTest, InputDati

def stima_z_score(bilancio: Bilancio):
    if not bilancio.totale_attivo or bilancio.totale_attivo == 0:
        return 0
    return round((bilancio.ebitda + bilancio.utile_netto) / bilancio.totale_attivo, 2)


def stima_mcc(bilancio: Bilancio):
    if not bilancio.ricavi or bilancio.ricavi == 0:
        return 0
    return round((bilancio.utile_netto / bilancio.ricavi) * 100, 2)

def converti_z_score_lettera(z_score: float) -> str:
    if z_score >= 2.5:
        return "A"
    elif 1.0 <= z_score < 2.5:
        return "B"
    else:
        return "C"

def converti_mcc_lettera(mcc: float) -> str:
    if mcc >= 7:
        return "A"
    elif 4 <= mcc < 7:
        return "B"
    else:
        return "C"
