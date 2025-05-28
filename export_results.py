
import pandas as pd
from datetime import datetime
import os

def export_to_csv(dataframe, output_dir="exported_data", filename_prefix="analisi_bilancio"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    dataframe.to_csv(filepath, index=False)
    return filepath

def export_to_excel(dataframe, output_dir="exported_data", filename_prefix="analisi_bilancio"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    dataframe.to_excel(filepath, index=False)
    return filepath

def export_to_json(dataframe, output_dir="exported_data", filename_prefix="analisi_bilancio"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    dataframe.to_json(filepath, orient="records", lines=True)
    return filepath
