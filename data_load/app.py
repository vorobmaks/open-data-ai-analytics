import urllib.request
import sqlite3
import os
from pathlib import Path
import pandas as pd

DATA_URL = "https://data.gov.ua/dataset/95c82130-4310-4edb-b7e5-f01b59385eb0/resource/caa8e037-3020-492d-9ca0-7db4429a0025/download/active_declarations_by_age_gender.csv"

DATA_DIR = Path("/app/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = DATA_DIR / "active_declarations_by_age_gender.csv"

DB_PATH = os.getenv("DB_PATH", "/app/db/data.db")
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

print("Downloading data...")
urllib.request.urlretrieve(DATA_URL, CSV_FILE)
print(f"Data saved to {CSV_FILE}")

df = pd.read_csv(CSV_FILE, encoding="utf-8")
df.columns = [c.strip() for c in df.columns]
print(f"Loaded {len(df)} rows, columns: {list(df.columns)}")

conn = sqlite3.connect(DB_PATH)

cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS declarations")
cur.execute("""
    CREATE TABLE declarations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        legal_entity_id TEXT,
        area TEXT,
        gromada_koatuu TEXT,
        gromada_name TEXT,
        settlement_koatuu TEXT,
        settlement TEXT,
        settlement_type TEXT,
        person_gender TEXT,
        person_age REAL,
        count_declarations INTEGER
    )
""")
conn.commit()

df["person_age"] = pd.to_numeric(df["person_age"], errors="coerce")
df["count_declarations"] = pd.to_numeric(df["count_declarations"], errors="coerce").fillna(0).astype(int)

df.to_sql("declarations", conn, if_exists="append", index=False,
          dtype={
              "legal_entity_id": "TEXT",
              "area": "TEXT",
              "gromada_koatuu": "TEXT",
              "gromada_name": "TEXT",
              "settlement_koatuu": "TEXT",
              "settlement": "TEXT",
              "settlement_type": "TEXT",
              "person_gender": "TEXT",
              "person_age": "REAL",
              "count_declarations": "INTEGER",
          })

conn.close()
print(f"Inserted {len(df)} rows into {DB_PATH}")