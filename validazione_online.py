
import random

# Elenco fonti autorevoli da usare nelle ricerche
FONTI_AUTOREVOLI = [
    "mise.gov.it",
    "invitalia.it",
    "incentivi.gov.it",
    "europa.eu",
    "fondieuropei.gov.it",
    "bandi.regione.lombardia.it",
    "regione.piemonte.it",
    "pnrr.gov.it",
    "filse.it",
    "ilsole24ore.com"
]

def valida_bando_online_mock(titolo_bando, regione=None):
    # Simula la verifica online con Google API (da implementare)
    # Qui usiamo mock: restituisce una validazione random per test

    validato = random.choice([True, True, False])  # Alta probabilità che sia valido
    fondi_disponibili = random.choice([True, True, False])  # Simula fondi presenti

    fonte = random.choice(FONTI_AUTOREVOLI) if validato else None
    messaggio = ""

    if validato:
        messaggio += f"✅ Validato online tramite {fonte}."
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
