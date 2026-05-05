from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPORTS_DIR = Path("/app/reports")
FIGURES_DIR = REPORTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_RESEARCH_DIR = REPORTS_DIR / "data_research"

plt.rcParams.update({
    "figure.facecolor": "#0a0e17",
    "axes.facecolor": "#111827",
    "axes.edgecolor": "#1e2d45",
    "text.color": "#e2e8f0",
    "axes.labelcolor": "#e2e8f0",
    "xtick.color": "#64748b",
    "ytick.color": "#64748b",
    "grid.color": "#1e2d45",
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
})

def plot_declarations_by_age():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_declarations_by_age.csv")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["person_age"], df["count_declarations"] / 1_000_000,
            color="#3b82f6", linewidth=2)
    ax.fill_between(df["person_age"], df["count_declarations"] / 1_000_000,
                    alpha=0.15, color="#3b82f6")
    ax.set_xlabel("Вік")
    ax.set_ylabel("Декларацій (млн)")
    ax.set_title("Кількість декларацій за віком", pad=15)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "declarations_by_age.png", dpi=120)
    plt.close(fig)
    print("Saved declarations_by_age.png")

def plot_gender_gap():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_gender_by_age.csv")
    df = df.sort_values("gender_gap", ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(df["person_age"].astype(str), df["gender_gap"] / 1000, color="#7c3aed")
    ax.set_xlabel("Вік")
    ax.set_ylabel("Гендерний розрив (тис.)")
    ax.set_title("Топ 20 вікових груп за гендерним розривом", pad=15)
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "gender_gap_by_age.png", dpi=120)
    plt.close(fig)
    print("Saved gender_gap_by_age.png")

def plot_top_regions():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_top_area.csv")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#3b82f6" if i == 0 else "#1e3a5f" for i in range(len(df))]
    bars = ax.barh(df["area"], df["count_declarations"] / 1_000_000, color=colors)
    ax.set_xlabel("Декларацій (млн)")
    ax.set_title("Топ регіонів за загальною кількістю декларацій", pad=15)
    ax.grid(True, axis="x")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "top_regions.png", dpi=120)
    plt.close(fig)
    print("Saved top_regions.png")

def plot_gender_by_age_lines():
    df = pd.read_csv(DATA_RESEARCH_DIR / "research_gender_by_age.csv")
    df = df.sort_values("person_age")
    fig, ax = plt.subplots(figsize=(12, 5))
    gender_cols = [c for c in df.columns if c not in ("person_age", "gender_gap")]
    colors_map = {"жіноча": "#ec4899", "чоловіча": "#3b82f6"}
    for col in gender_cols:
        ax.plot(df["person_age"], df[col] / 1000,
                label=col, color=colors_map.get(col, "#aaa"), linewidth=2)
    ax.set_xlabel("Вік")
    ax.set_ylabel("Декларацій (тис.)")
    ax.set_title("Декларації за статтю та віком", pad=15)
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "gender_by_age_lines.png", dpi=120)
    plt.close(fig)
    print("Saved gender_by_age_lines.png")

plot_declarations_by_age()
plot_gender_gap()
plot_top_regions()
plot_gender_by_age_lines()
print("All visualizations saved to /app/reports/figures/")
