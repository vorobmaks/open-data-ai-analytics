from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_RESEARCH_DIR = REPORTS_DIR / "data_research"

def plot_declarations_by_age():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_declarations_by_age.csv")

    plt.figure(figsize=(10, 5))
    plt.plot(df["person_age"], df["count_declarations"])
    plt.xlabel("Age")
    plt.ylabel("Number of declarations")
    plt.title("Declarations by Age")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "declarations_by_age.png")
    plt.close()

def plot_gender_gap():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_gender_by_age.csv")
    df = df.sort_values("gender_gap", ascending=False).head(15)

    plt.figure(figsize=(10, 5))
    plt.bar(df["person_age"], df["gender_gap"])
    plt.xlabel("Age")
    plt.ylabel("Gender gap")
    plt.title("Top age groups by gender gap")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "gender_gap_by_age.png")
    plt.close()

def plot_top_regions():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_top_area_age.csv")

    plt.figure(figsize=(10, 5))
    labels = df["area"] + " (" + df["person_age"].astype(str) + ")"
    plt.barh(labels, df["count_declarations"])
    plt.xlabel("Number of declarations")
    plt.title("Top regions and age groups by declarations")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_regions_by_age.png")
    plt.close()

plot_declarations_by_age()
plot_gender_gap()
plot_top_regions()
print("Visualizations saved to reports/figures/")