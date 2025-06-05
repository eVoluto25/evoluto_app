def detect_file_type(file_path):
    ext = Path(file_path).suffix.lower()
    return ext


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def estrai_da_xbrl(file_path):
    data = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'ns': root.tag.split('}')[0].strip('{')}  # Detect namespace dynamically

        for tag in ['Ricavi', 'EBITDA', 'UtileNetto', 'Debiti', 'TotaleAttivo', 'TotalePassivo', 'PatrimonioNetto']:
            for elem in root.findall(f".//ns:{tag}", ns):
                value = elem.text
                if value and value.replace(',', '').replace('.', '').isdigit():
                    data[tag.lower()] = float(value.replace(',', '.'))
    except Exception as e:
        data['error'] = str(e)
    return data


def estrai_da_pdf(file_path):
    data = {}
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        text = clean_text(text)
        # Estrai numeri base da pattern comuni
        patterns = {
            'ricavi': r"ricavi.*?([\d.,]+)",
            'ebitda': r"ebitda.*?([\d.,]+)",
            'utile_netto': r"utile netto.*?([\d.,]+)",
            'debiti': r"debiti.*?([\d.,]+)"
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).replace('.', '').replace(',', '.')
                try:
                    data[key] = float(value)
                except:
                    continue
    except Exception as e:
        data['error'] = str(e)
    return data


def estrai_da_csv(file_path):
    data = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for field in row:
                    key_val = field.strip().split(":")
                    if len(key_val) == 2:
                        key, val = key_val
                        key = key.strip().lower()
                        try:
                            val = float(val.replace('.', '').replace(',', '.'))
                            data[key] = val
                        except:
                            continue
    except Exception as e:
        data['error'] = str(e)
    return data


def estrai_da_txt(file_path):
    return estrai_da_csv(file_path)  # Assume lo stesso formato


def estrai_dati(file_path):
    ext = detect_file_type(file_path)
    if ext in ['.xbrl', '.xml']:
        return estrai_da_xbrl(file_path)
    elif ext == '.pdf':
        return estrai_da_pdf(file_path)
    elif ext in ['.csv', '.txt']:
        return estrai_da_csv(file_path)
    else:
        raise ValueError("Formato file non supportato.")
