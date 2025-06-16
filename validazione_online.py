import random

# Elenco fonti autorevoli da usare nelle ricerche
FONTI_AUTOREVOLI = [
    "invitalia.it",
    "mise.gov.it",
    "incentivi.gov.it",
    "fondieuropei.gov.it",
    "pnrr.gov.it",
    "italiadomani.gov.it",
    "regione.lombardia.it",
    "regione.veneto.it",
    "regione.piemonte.it",
    "regione.emilia-romagna.it",
    "regione.toscana.it",
    "regione.lazio.it",
    "regione.campania.it",
    "regione.puglia.it",
    "regione.sardegna.it",
    "regione.sicilia.it",
    "regione.abruzzo.it",
    "regione.basilicata.it",
    "regione.calabria.it",
    "regione.fvg.it",
    "regione.marche.it",
    "regione.molise.it",
    "regione.umbria.it",
    "regione.vda.it",
    "provincia.bz.it"
]

def valida_bando_online_mock(titolo_bando, regione=None):
    # Simula la verifica online con Google API (da implementare)
    # Qui usiamo mock: restituisce una validazione random per test

    validato = random.choice([True, True, False])  # Alta probabilità che sia valido
    fondi_disponibili = random.choice([True, True, False])  # Simula fondi presenti

    fonte = random.choice(FONTI_AUTOREVOLI) if validato else None
    messaggio = ""

    if validato:
        messaggio += f"✅ Validato online da fonti ufficiali."
    else:
        messaggio += "⚠️ Non validato da fonti ufficiali."

    if fondi_disponibili:
        messaggio += " 💰 Fondi ancora disponibili secondo fonti pubbliche."
    else:
        messaggio += " ❌ Fondi risultano esauriti o non verificabili."

    return {
        "validato": validato,
        "fondi_disponibili": fondi_disponibili,
        "fonte": fonte,
        "messaggio": messaggio
    }
