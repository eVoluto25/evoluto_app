def simula_beneficio(bando, bilancio):
    def calcola_fondo_perduto(investimento):
        fondo = investimento * 0.5
        return {
            "agevolazione_ottenibile": round(fondo, 2),
            "liquidita_migliorata": f"{fondo:,.0f} €"
        }

    def calcola_credito_imposta(investimento, aliquota):
        credito = investimento * 0.4
        risparmio = credito * aliquota
        return {
            "agevolazione_ottenibile": round(credito, 2),
            "risparmio_fiscale": f"{risparmio:,.0f} €"
        }

    def calcola_finanziamento(investimento, ebitda, tasso=0.01, durata=5):
        rata = (investimento * tasso * (1 + tasso) ** durata) / (((1 + tasso) ** durata) - 1)
        cashflow_post = ebitda - rata
        return {
            "agevolazione_ottenibile": round(investimento, 2),
            "rata_annua": round(rata, 2),
            "cashflow_post_intervento": f"{cashflow_post:,.0f} €"
        }

    def calcola_redditivita(ebitda, utile, investimento):
        incremento = investimento * 0.2
        return {
            "ebitda_potenziale": f"{ebitda + incremento:,.0f} €",
            "utile_potenziale": f"{utile + incremento:,.0f} €"
        }

    # ----> Dati iniziali
    risultato = {
        "bando": bando.get("titolo", "N/D"),
        "tipo_agevolazione": bando.get("forma_agevolazione", "N/D"),
        "investimento": bando.get("spesa_ammessa", 0)
    }

    investimento = risultato["investimento"] or 0
    tipo = risultato["tipo_agevolazione"].lower()

    utile = bilancio.get("utile_netto", 0)
    ebitda = bilancio.get("ebitda", 0)
    aliquota = 0.27

    # ----> Calcolo agevolazione
    if "fondo perduto" in tipo:
        risultato.update(calcola_fondo_perduto(investimento))

    elif "credito imposta" in tipo:
        risultato.update(calcola_credito_imposta(investimento, aliquota))

    elif "finanziamento" in tipo:
        risultato.update(calcola_finanziamento(investimento, ebitda))

    # ----> Calcolo potenziale strategico sempre
    risultato.update(calcola_redditivita(ebitda, utile, investimento))

    return risultato
