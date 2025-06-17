from validazione_google import cerca_google_bando

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

def valida_bando_online(titolo_bando, regione=None):
    try:
        risposta = cerca_google_bando(titolo_bando, regione)
        return {
            "validato": risposta.get("validato", False),
            "fondi_disponibili": risposta.get("fondi_disponibili", False),
            "fonte": risposta.get("fonte", "N/D"),
            "messaggio": risposta.get("messaggio", "⚠️ Nessuna informazione disponibile.")
        }
    except Exception as e:
        return {
            "validato": False,
            "fondi_disponibili": False,
            "fonte": None,
            "messaggio": f"❌ Errore durante la validazione: {str(e)}"
        }
