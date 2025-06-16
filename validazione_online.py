import random

# Elenco fonti autorevoli da usare nelle ricerche
FONTI_AUTOREVOLI = [
    # Ministeri e agenzie nazionali
    "mise.gov.it",
    "invitalia.it",
    "incentivi.gov.it",
    "fondieuropei.gov.it",
    "pnrr.gov.it",
    "italiadomani.gov.it",

    # Portali europei
    "europa.eu",
    "ec.europa.eu",

    # Portali Regioni
    "bandi.regione.abruzzo.it",
    "bandi.regione.basilicata.it",
    "bandi.regione.calabria.it",
    "bandi.regione.campania.it",
    "bandi.regione.emilia-romagna.it",
    "bandi.regione.fvg.it",  # Friuli Venezia Giulia
    "filse.it",  # Liguria (agenzia)
    "bandi.regione.lazio.it",
    "bandi.regione.lombardia.it",
    "bandi.regione.marche.it",
    "regione.molise.it",
    "regione.piemonte.it",
    "bandi.regione.puglia.it",
    "bandi.regione.sardegna.it",
    "bandi.regione.sicilia.it",
    "regione.taa.it",  # Trentino-Alto Adige
    "bandi.regione.toscana.it",
    "bandi.regione.umbria.it",
    "bandi.regione.veneto.it",
    "regione.vda.it",  # Valle d'Aosta
    "svemmarche.it"  # alternativa per Marche

    # Fonti informative autorevoli
    "ilsole24ore.com",
    "agendadigitale.eu",
    "startmag.it",
    "quifinanza.it"
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
