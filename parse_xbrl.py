import xml.etree.ElementTree as ET

def parse_xbrl_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {
        'xbrli': 'http://www.xbrl.org/2003/instance',
        'itcc-ci': 'http://www.frc.org.uk/xbrl/itcc-ci/2005-12-01',
        'itcc': 'http://www.frc.org.uk/xbrl/itcc/2005-12-01'
    }

    data = {
        "anagrafica": {},
        "contabili": {}
    }

    # Anagrafica
    for tag, key in {
        'DenominazioneImpresa': 'denominazione',
        'ComuneSedeLegale': 'comune_sede_legale',
        'ProvinciaSedeLegale': 'provincia_sede_legale',
        'CodiceATECO': 'codice_ateco',
        'DataCostituzione': 'data_costituzione'
    }.items():
        elem = root.find(f".//itcc-ci:{tag}", ns)
        if elem is not None and elem.text:
            data["anagrafica"][key] = elem.text

    # Contabili
    for tag, key in {
        'NumeroDipendenti': 'numero_dipendenti',
        'RicaviVenditeNetti': 'fatturato',
        'TotaleAttivo': 'totale_attivo',
        'DisponibilitaLiquide': 'disponibilita_liquide',
        'UtilePerditaEsercizio': 'utile_netto',
        'ImmobilizzazioniMateriali': 'immobilizzazioni_materiali',
        'ImmobilizzazioniImmateriali': 'immobilizzazioni_immateriali',
        'SpeseRicercaSviluppo': 'spese_rs',
        'Debiti': 'indebitamento'
    }.items():
        elem = root.find(f".//itcc:{tag}", ns)
        if elem is not None and elem.text:
            try:
                data["contabili"][key] = float(elem.text.replace(',', '.'))
            except ValueError:
                data["contabili"][key] = elem.text

    return data
