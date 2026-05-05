import sqlite3
import json
import csv
import os
from pathlib import Path

DB_PATH = os.getenv("DB_PATH", "/app/db/data.db")
REPORTS_DIR = Path("/app/reports/data_research")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- declarations by age (sum across all areas/genders) ---
cur.execute("""
    SELECT person_age, SUM(count_declarations) as total
    FROM declarations
    WHERE person_age IS NOT NULL
    GROUP BY person_age
    ORDER BY person_age
""")
by_age = [{"person_age": r[0], "count_declarations": r[1]} for r in cur.fetchall()]

# --- gender breakdown by age ---
cur.execute("""
    SELECT person_age, person_gender, SUM(count_declarations) as total
    FROM declarations
    WHERE person_age IS NOT NULL AND person_gender != ''
    GROUP BY person_age, person_gender
    ORDER BY person_age
""")
rows = cur.fetchall()

age_gender = {}
for age, gender, total in rows:
    if age not in age_gender:
        age_gender[age] = {}
    age_gender[age][gender] = total

gender_gap_rows = []
for age in sorted(age_gender.keys()):
    gmap = age_gender[age]
    vals = list(gmap.values())
    gap = max(vals) - min(vals) if len(vals) >= 2 else 0
    entry = {"person_age": age, "gender_gap": gap}
    entry.update(gmap)
    gender_gap_rows.append(entry)
gender_gap_rows.sort(key=lambda x: x["gender_gap"], reverse=True)

# --- top regions by total declarations ---
cur.execute("""
    SELECT area, SUM(count_declarations) as total
    FROM declarations
    WHERE area != ''
    GROUP BY area
    ORDER BY total DESC
    LIMIT 10
""")
top_area = [{"area": r[0], "count_declarations": r[1]} for r in cur.fetchall()]

# --- top area+age combos ---
cur.execute("""
    SELECT area, person_age, SUM(count_declarations) as total
    FROM declarations
    WHERE area != '' AND person_age IS NOT NULL
    GROUP BY area, person_age
    ORDER BY total DESC
    LIMIT 10
""")
top_area_age = [{"area": r[0], "person_age": r[1], "count_declarations": r[2]} for r in cur.fetchall()]

# --- summary stats ---
cur.execute("SELECT SUM(count_declarations), AVG(count_declarations), COUNT(DISTINCT area) FROM declarations")
sum_count, avg_count, unique_areas = cur.fetchone()

conn.close()

# Write CSVs
def write_csv(path, data, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(data)

write_csv(REPORTS_DIR / "research_declarations_by_age.csv",
          by_age, ["person_age", "count_declarations"])

gender_fields = list(gender_gap_rows[0].keys()) if gender_gap_rows else ["person_age", "gender_gap"]
write_csv(REPORTS_DIR / "research_gender_by_age.csv", gender_gap_rows, gender_fields)

write_csv(REPORTS_DIR / "research_top_area.csv", top_area, ["area", "count_declarations"])
write_csv(REPORTS_DIR / "research_top_area_age.csv", top_area_age, ["area", "person_age", "count_declarations"])

# Top age by declarations
top_age = max(by_age, key=lambda x: x["count_declarations"]) if by_age else {}
top_gap = gender_gap_rows[0] if gender_gap_rows else {}

metrics = {
    "total_declarations": int(sum_count) if sum_count else 0,
    "avg_declarations_per_record": round(avg_count, 2) if avg_count else 0,
    "unique_areas": int(unique_areas) if unique_areas else 0,
    "top_age_by_declarations": top_age,
    "top_gender_gap_age": top_gap,
}

(REPORTS_DIR / "model_metrics.json").write_text(
    json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
(REPORTS_DIR / "model_metrics.txt").write_text(
    f"Total declarations: {metrics['total_declarations']:,}\n"
    f"Avg per record: {metrics['avg_declarations_per_record']}\n"
    f"Unique areas: {metrics['unique_areas']}\n"
    f"Top age by declarations: age={top_age.get('person_age')}, count={top_age.get('count_declarations'):,}\n"
    f"Largest gender gap: age={top_gap.get('person_age')}, gap={top_gap.get('gender_gap'):,}\n",
    encoding="utf-8"
)

print("Data research done. Reports saved.")
