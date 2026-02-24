import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

DATA_FILE = RAW_DIR / "active_declarations_by_age_gender.csv"

df = pd.read_csv(DATA_FILE, encoding="utf-8")

report = []
report.append(f"Rows: {len(df)}")
report.append(f"Columns: {df.shape[1]}")
report.append("\nMissing values:")
report.append(df.isna().sum().to_string())
report.append("\nDuplicate rows:")
report.append(str(df.duplicated().sum()))
report.append("\nData types:")
report.append(df.dtypes.to_string())

report_path = REPORTS_DIR / "data_quality_report.txt"
report_path.write_text("\n".join(report), encoding="utf-8")

print(f"Data quality report saved to {report_path}")
