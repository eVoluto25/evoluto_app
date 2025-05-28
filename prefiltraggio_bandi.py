
def prefiltra_bandi(bandi, azienda):
    bandi_filtrati = []

    for bando in bandi:
        # Filtro per settore ATECO
        if 'ateco' in azienda and azienda['ateco'] not in bando.get('settori_ammissibili', []):
            continue

        # Filtro per regione
        if 'regione' in azienda and azienda['regione'] not in bando.get('regioni_ammissibili', []):
            continue

        # Filtro per dimensione d'impresa
        if 'dimensione' in azienda and azienda['dimensione'] not in bando.get('dimensioni_ammissibili', []):
            continue

        # Filtro per soggetto ammissibile
        if 'forma_giuridica' in azienda and azienda['forma_giuridica'] not in bando.get('soggetti_ammissibili', []):
            continue

        bandi_filtrati.append(bando)

    return bandi_filtrati
