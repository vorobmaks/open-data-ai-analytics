## Мета
Проаналізувати відкритий набір даних у сфері охорони здоровʼя України, а саме —
дослідження розподілу активних декларацій пацієнтів з лікарями залежно від віку, статі та регіону.  
Проєкт включає етапи завантаження даних, перевірки їх якості, дослідження та
візуалізації результатів.

## Джерела
Портал відкритих даних України: https://data.gov.ua/
Набір даних: https://data.gov.ua/dataset/a8228262-5576-4a14-beb8-789573573546

## Питання для аналізу
1. Яка вікова група має найбільший гендерний розрив у кількості активних декларацій?
2. Як змінюється кількість активних декларацій зі зростанням віку пацієнтів?
3. Які регіони демонструють найбільшу концентрацію декларацій серед окремих вікових груп?

## Структура проєкту
```
project/
├── data_load/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── data_quality_analysis/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── data_research/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── visualization/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── web/
│   ├── app.py
│   ├── templates/
│   ├── Dockerfile
│   └── requirements.txt
├── compose.yaml
├── .env
├── .gitignore
└── README.md
```

## Опис сервісів
| Сервіс | Опис                                                                 | Порт |
|---|----------------------------------------------------------------------|---|
| `data_load` | Завантажує CSV з data.gov.ua, записує у SQLite                       | — |
| `data_quality_analysis` | Аналізує якість даних (пропуски, дублікати, типи), зберігає TXT+JSON | — |
| `data_research` | Обчислює статистики, зберігає CSV+JSON звіти                         | — |
| `visualization` | Будує 4 графіки PNG                                                  | — |
| `web` | Flask-веб-інтерфейс для перегляду результатів                        | **5000** |

## Команди запуску
```bash
# Запустити всі сервіси
docker compose up --build

# Фоновий режим
docker compose up --build -d

# Список контейнерів
docker compose ps

# Логи
docker compose logs -f

# Зупинити
docker compose down

# Зупинити + видалити томи
docker compose down -v
```

Після запуску відкрийте: **http://localhost:5000**


## Взаємодія між сервісами
- **`db-data`** (том) — SQLite база даних, яку пише `data_load` і читають `data_quality_analysis`, `data_research`, `web`
- **`reports-data`** (том) — звіти та графіки, що передаються між `data_quality_analysis` → `web`, `data_research` → `visualization` → `web`
- **`app-net`** (bridge мережа) — єдина мережа для всіх контейнерів
- **`depends_on`** — забезпечує порядок запуску: data_load → quality/research → visualization → web

## Healthcheck
Сервіс `web` має healthcheck (перевірка кожні 30с, таймаут 10с, 3 спроби).

## Моніторинг (Prometheus + Grafana)

### Структура
```
monitoring/
├── prometheus/
│   └── prometheus.yml
├── grafana/
│   ├── dashboards/
│   │   └── main-dashboard.json
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           └── dashboards.yml
└── docker-compose.monitoring.yml
```

### Сервіси моніторингу
| Сервіс | Опис | Порт |
|---|---|---|
| `prometheus` | Збір та зберігання метрик | 9090 |
| `grafana` | Візуалізація та дашборди | **3000** |
| `node-exporter` | Метрики Linux VM (CPU, RAM, диск, мережа) | — |
| `cadvisor` | Метрики Docker-контейнерів | — |

### Джерела метрик (scrape jobs)
- **prometheus** — самомоніторинг Prometheus
- **node-exporter** — стан VM: CPU, пам'ять, диск, мережа
- **cadvisor** — стан контейнерів: CPU, пам'ять на контейнер
- **web-app** — метрики Flask-застосунку через `/metrics` (`web_requests_total`, `web_request_duration_seconds`)

### Відкриті порти на Azure VM
| Порт | Призначення |
|---|---|
| 22 | SSH |
| 5000 | Веб-застосунок |
| 3000 | Grafana |
| 9090 | Prometheus |

### Як розгортається моніторинг
Моніторинг запускається автоматично через `cloud-init` після старту основного стеку:
```bash
docker compose -f /opt/app/monitoring/docker-compose.monitoring.yml up -d
```
Стек моніторингу підключається до мережі `open-data-analytics_app-net`, щоб мати доступ до контейнера `web`.

### Як відкрити Grafana
```
http://<PUBLIC_IP>:3000
```
- Логін: `admin`
- Пароль: `admin123`

Datasource Prometheus підключається автоматично через provisioning (`http://prometheus:9090`).

### Дашборд — панелі
Дашборд **"Open Data AI Analytics — System Monitoring"** завантажується автоматично і містить 8 панелей:

| # | Панель | Тип | Метрика |
|---|---|---|---|
| 1 | CPU Usage — VM | timeseries | `node_cpu_seconds_total` |
| 2 | Memory Usage — VM | timeseries | `node_memory_MemTotal/Available_bytes` |
| 3 | Running Containers | stat | `container_last_seen` |
| 4 | Total Memory — VM | stat | `node_memory_MemTotal_bytes` |
| 5 | Disk Usage — Root Filesystem | gauge | `node_filesystem_size/free_bytes` |
| 6 | CPU Usage — web container | timeseries | `container_cpu_usage_seconds_total` |
| 7 | Memory Usage — web container | timeseries | `container_memory_usage_bytes` |
| 8 | Network I/O — VM | timeseries | `node_network_receive/transmit_bytes_total` |
