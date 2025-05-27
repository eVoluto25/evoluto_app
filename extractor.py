import PyPDF2

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_data_from_pdf(visura_file, bilancio_file):
    visura_text = extract_text_from_pdf(visura_file)
    bilancio_text = extract_text_from_pdf(bilancio_file)

    azienda_data = {
        "denominazione": "ACME S.p.A.",
        "amministratore": "Mario Rossi",
        "codice_ateco": "62.01.00",
        "forma_giuridica": "S.p.A.",
        "cap": "20100",
        "provincia": "MI",
        "dipendenti": 12,
        "fatturato": 1500000,
        "totale_attivo": 2300000,
        "utile_netto": 120000,
        "ebitda": 240000,
        "beni_strumentali": 80000,
        "ricerca_sviluppo": 25000,
        "sede_legale": "Milano",
        "data_costituzione": "2005-03-21",
        "bilancio_testo": bilancio_text
    }

    return azienda_data
