from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "active_declarations_by_age_gender.csv"
REPORTS_DIR = PROJECT_ROOT / "reports" / "data_research"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE, encoding="utf-8")
    df.columns = [c.strip() for c in df.columns]

    needed = ["area", "person_gender", "person_age", "count_declarations"]
    df = df.dropna(subset=needed)

    df["person_age"] = pd.to_numeric(df["person_age"], errors="coerce")
    df["count_declarations"] = pd.to_numeric(df["count_declarations"], errors="coerce")
    df = df.dropna(subset=["person_age", "count_declarations"])
    df = df[df["person_age"] >= 0]

    return df

def analysis(df: pd.DataFrame):
    gender_by_age = (
        df.groupby(["person_age", "person_gender"])["count_declarations"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )

    if gender_by_age.shape[1] >= 2:
        gender_by_age["gender_gap"] = (
            gender_by_age.max(axis=1) - gender_by_age.min(axis=1)
        )
        max_gap_age = gender_by_age["gender_gap"].idxmax()
    else:
        max_gap_age = None

    declarations_by_age = (
        df.groupby("person_age")["count_declarations"]
        .sum()
        .sort_index()
    )

    top_area_age = (
        df.groupby(["area", "person_age"])["count_declarations"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    gender_by_age.to_csv(REPORTS_DIR / "research_gender_by_age.csv")
    declarations_by_age.to_csv(REPORTS_DIR / "research_declarations_by_age.csv")
    top_area_age.to_csv(REPORTS_DIR / "research_top_area_age.csv", index=False)

def build_random_forest(df: pd.DataFrame):
    X = df[["area", "person_gender", "person_age"]]
    y = df["count_declarations"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["area", "person_gender"]),
            ("num", "passthrough", ["person_age"]),
        ]
    )

    model = Pipeline(
        steps=[
            ("prep", preprocessor),
            ("rf", RandomForestRegressor(
                n_estimators=50,
                max_depth=8,
                random_state=42,
                n_jobs=-1
            )),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = [
        "Model: Random Forest Regressor",
        f"MAE: {mae:.4f}",
        f"R2: {r2:.4f}",
        "Features: area, person_gender, person_age",
    ]

    (REPORTS_DIR / "model_metrics.txt").write_text(
        "\n".join(metrics), encoding="utf-8"
    )

df = load_data()
analysis(df)
build_random_forest(df)
print("Done. See reports/data_research/ directory.")
