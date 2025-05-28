
import json
import pandas as pd
from pathlib import Path

def export_company_profile(data: dict, output_path: str = "data/company_profile.json"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

def export_financial_analysis(analysis: dict, output_path: str = "data/financial_analysis.json"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(analysis, f, indent=4)

def export_bandi_results(results: list, output_path: str = "data/bandi_results.csv"):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
