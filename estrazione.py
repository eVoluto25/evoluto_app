def estrai_indici(dati):
    try:
        fatturato = float(dati.get("fatturato_annuo", 0))
        utile_netto = float(dati.get("utile_netto", 0))
        ebitda = float(dati.get("ebitda", 0))
        spese_r_s = float(dati.get("spese_r_s", 0))
        costi_ambientali = float(dati.get("costi_ambientali", 0))
        totale_attivo = float(dati.get("totale_attivo", 1))
        disponibilita_liquide = float(dati.get("disponibilita_liquide", 0))
        immobilizzazioni = float(dati.get("immobilizzazioni", 0))
        indebitamento = float(dati.get("indebitamento", 0))
        oneri_finanziari = float(dati.get("oneri_finanziari", 1))
        ammortamenti = float(dati.get("ammortamenti", 0))
        investimenti_recenti = float(dati.get("investimenti_recenti", 0))

        patrimonio_netto = max(totale_attivo - indebitamento, 1)

        return {
            "fatturato_annuo": fatturato,
            "utile_netto": utile_netto,
            "ebitda": ebitda,
            "ebitda_margin": ebitda / fatturato if fatturato else 0,
            "spese_r_s": spese_r_s,
            "costi_ambientali": costi_ambientali,
            "totale_attivo": totale_attivo,
            "disponibilita_liquide": disponibilita_liquide,
            "immobilizzazioni": immobilizzazioni,
            "indebitamento": indebitamento,
            "debt_equity_ratio": indebitamento / patrimonio_netto if patrimonio_netto else 0,
            "current_ratio": disponibilita_liquide / indebitamento if indebitamento else 0,
            "interest_coverage_ratio": ebitda / oneri_finanziari if oneri_finanziari else 0,
            "capacita_autofinanziamento": utile_netto + ammortamenti,
            "investimenti_recenti": investimenti_recenti
        }
    except Exception as e:
        raise ValueError(f"Errore nel calcolo indici: {e}")

def assegna_macroarea(indici):
    crisi = (
        indici["current_ratio"] < 1 or
        indici["debt_equity_ratio"] > 2 or
        indici["interest_coverage_ratio"] < 1 or
        indici["ebitda_margin"] < 0 or
        indici["utile_netto"] < 0
    )

    crescita = (
        indici["capacita_autofinanziamento"] > 0 and
        (indici["totale_attivo"] - indici["indebitamento"]) / indici["totale_attivo"] > 0.2 and
        indici["immobilizzazioni"] / indici["totale_attivo"] > 0.2
    )

    if crisi:
        return "area_crisi_risanamento"
    elif crescita:
        return "area_crescita_sviluppo"
    else:
        return "area_espansione_transizione"
