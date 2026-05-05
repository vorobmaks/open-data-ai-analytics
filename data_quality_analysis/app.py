import sqlite3
import json
import os
from pathlib import Path

DB_PATH = os.getenv("DB_PATH", "/app/db/data.db")
REPORTS_DIR = Path("/app/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM declarations")
total_rows = cur.fetchone()[0]

cur.execute("PRAGMA table_info(declarations)")
col_info = {row[1]: row[2] for row in cur.fetchall() if row[1] != "id"}
total_columns = len(col_info)

# Missing values
missing = {}
for col in col_info:
    cur.execute(f"SELECT COUNT(*) FROM declarations WHERE {col} IS NULL OR CAST({col} AS TEXT) = ''")
    missing[col] = cur.fetchone()[0]

# Рядки де person_age IS NULL (були "100+" в CSV)
cur.execute("SELECT COUNT(*) FROM declarations WHERE person_age IS NULL")
age_100plus_count = cur.fetchone()[0]

# Duplicates
cur.execute("""
    SELECT COUNT(*) FROM (
        SELECT legal_entity_id, area, gromada_koatuu, gromada_name,
               settlement_koatuu, settlement, settlement_type,
               person_gender, person_age, count_declarations,
               COUNT(*) as cnt
        FROM declarations
        GROUP BY legal_entity_id, area, gromada_koatuu, gromada_name,
                 settlement_koatuu, settlement, settlement_type,
                 person_gender, person_age, count_declarations
        HAVING cnt > 1
    )
""")
duplicates = cur.fetchone()[0]

cur.execute("SELECT COUNT(DISTINCT area) FROM declarations")
unique_areas = cur.fetchone()[0]

cur.execute("SELECT DISTINCT person_gender FROM declarations WHERE person_gender != ''")
genders = [r[0] for r in cur.fetchall()]

cur.execute("SELECT MIN(person_age), MAX(person_age), AVG(person_age) FROM declarations WHERE person_age IS NOT NULL")
age_stats = cur.fetchone()

cur.execute("SELECT MIN(count_declarations), MAX(count_declarations), AVG(count_declarations) FROM declarations")
count_stats = cur.fetchone()

conn.close()

report_json = {
    "total_rows": total_rows,
    "total_columns": total_columns,
    "missing_values": missing,
    "age_100plus_rows": age_100plus_count,
    "duplicates": duplicates,
    "unique_areas": unique_areas,
    "unique_genders": genders,
    "age_stats": {
        "min": age_stats[0],
        "max": age_stats[1],
        "avg": round(age_stats[2], 2) if age_stats[2] else None,
        "note": f"Excluded {age_100plus_count} rows with age '100+' (stored as NULL)"
    },
    "count_declarations_stats": {
        "min": count_stats[0],
        "max": count_stats[1],
        "avg": round(count_stats[2], 2) if count_stats[2] else None,
    },
    "column_types": col_info,
}

txt_lines = [
    f"Rows: {total_rows}",
    f"Columns: {total_columns}",
    "",
    "Missing values:",
] + [f"  {col}: {val}" for col, val in missing.items()] + [
    "",
    f"Примітка: person_age містить '100+' у {age_100plus_count} рядках — збережено як NULL",
    "",
    f"Duplicate rows: {duplicates}",
    "",
    f"Unique areas: {unique_areas}",
    f"Unique genders: {genders}",
    "",
    "Age stats (без 100+):",
    f"  min={age_stats[0]}, max={age_stats[1]}, avg={round(age_stats[2], 2) if age_stats[2] else 'N/A'}",
    "",
    "Count_declarations stats:",
    f"  min={count_stats[0]}, max={count_stats[1]}, avg={round(count_stats[2], 2) if count_stats[2] else 'N/A'}",
]

(REPORTS_DIR / "data_quality_report.txt").write_text("\n".join(txt_lines), encoding="utf-8")
(REPORTS_DIR / "data_quality_report.json").write_text(
    json.dumps(report_json, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("Data quality report saved.")
print("\n".join(txt_lines))