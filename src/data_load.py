import urllib.request
from pathlib import Path

DATA_URL = "https://data.gov.ua/dataset/95c82130-4310-4edb-b7e5-f01b59385eb0/resource/caa8e037-3020-492d-9ca0-7db4429a0025/download/active_declarations_by_age_gender.csv"

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

output_file = RAW_DIR / "active_declarations_by_age_gender.csv"

print("Downloading data...")
urllib.request.urlretrieve(DATA_URL, output_file)
print(f"Data saved to {output_file}")
