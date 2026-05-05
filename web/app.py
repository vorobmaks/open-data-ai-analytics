import sqlite3
import json
import os
from pathlib import Path
from flask import Flask, render_template, send_from_directory, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

DB_PATH = os.getenv("DB_PATH", "/app/db/data.db")
REPORTS_DIR = Path("/app/reports")
FIGURES_DIR = REPORTS_DIR / "figures"

# --- Метрики ---
REQUEST_COUNT = Counter(
    'web_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'web_request_duration_seconds',
    'HTTP request latency in seconds',
    ['endpoint']
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Middleware для автоматичного збору метрик ---
@app.before_request
def before_request():
    request._start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request._start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    return response

# --- Endpoint для Prometheus ---
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data_page():
    try:
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM declarations ORDER BY count_declarations DESC LIMIT 100"
        ).fetchall()
        conn.close()
    except Exception:
        rows = []
    return render_template("data.html", rows=rows)

@app.route("/quality")
def quality():
    report = {}
    txt = ""
    try:
        report_path = REPORTS_DIR / "data_quality_report.json"
        if report_path.exists():
            report = json.loads(report_path.read_text(encoding="utf-8"))
        txt_path = REPORTS_DIR / "data_quality_report.txt"
        if txt_path.exists():
            txt = txt_path.read_text(encoding="utf-8")
    except Exception:
        pass
    return render_template("quality.html", report=report, txt=txt)

@app.route("/research")
def research():
    metrics = {}
    txt = ""
    try:
        m_path = REPORTS_DIR / "data_research" / "model_metrics.json"
        if m_path.exists():
            metrics = json.loads(m_path.read_text(encoding="utf-8"))
        t_path = REPORTS_DIR / "data_research" / "model_metrics.txt"
        if t_path.exists():
            txt = t_path.read_text(encoding="utf-8")
    except Exception:
        pass
    return render_template("research.html", metrics=metrics, txt=txt)

@app.route("/visualization")
def visualization():
    figures = []
    try:
        if FIGURES_DIR.exists():
            figures = [f.name for f in sorted(FIGURES_DIR.glob("*.png"))]
    except Exception:
        pass
    return render_template("visualization.html", figures=figures)

@app.route("/figures/<path:filename>")
def figures(filename):
    return send_from_directory(str(FIGURES_DIR), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
