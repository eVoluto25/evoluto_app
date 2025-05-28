
import os
import json
import datetime
import logging
from lxml import etree

def setup_logging(log_file='extractor.log'):
    logging.basicConfig(filename=log_file,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

def extract_xbrl_data(file_path):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()
        data = {}
        for element in root.iter():
            if element.text and element.text.strip():
                data[element.tag] = element.text.strip()
        logging.info(f"Successfully extracted data from XBRL: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error parsing XBRL file: {file_path} - {str(e)}")
        return {}

def extract_visura_data(file_path):
    try:
        data = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
        logging.info(f"Successfully extracted data from Visura: {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error parsing Visura file: {file_path} - {str(e)}")
        return {}

def save_json(data, output_dir='extracted_data', prefix='data'):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f"{prefix}_{timestamp}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    logging.info(f"Data saved to {output_path}")
    return output_path

def extract_data(xbrl_file, visura_file):
    setup_logging()
    data = {}
    if xbrl_file:
        data['xbrl'] = extract_xbrl_data(xbrl_file)
    if visura_file:
        data['visura'] = extract_visura_data(visura_file)
    output_path = save_json(data)
    return output_path
