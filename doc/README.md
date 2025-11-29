# Mini Zenseact Pipeline – Home Assistant → Event-Based Data Platform

This project is a personal exploration of how to build a modern, event-driven data pipeline inspired by the data infrastructure patterns used in advanced automotive data platforms.  
The system ingests telemetry from **Home Assistant**, publishes changes as events, processes them, stores metrics in **PostgreSQL**, and makes them available for **Grafana analytics** and later for **Kafka-based streaming**, **OpenLineage tracking**, and **DataHub metadata registry**.

---

## 🚀 Goals

- Replace legacy **cron-based ingestion** with **real-time events**
- Introduce **Kafka (KRaft)** for scalable event streaming
- Use **Airflow 3 event-based DAG triggers**
- Add **OpenTelemetry** for distributed tracing + structured logging
- Track metadata and lineage using **OpenLineage**
- Register datasets and pipelines into **DataHub**
- Provide a small-scale but modern version of a **production-grade pipeline**

---

## 🏗️ Current Architecture (Phase 1)

Home Assistant
│
▼
MQTT (Mosquitto)
│
▼
ha_ingest.py → JSON event
│
▼
PostgreSQL (table: ha_sensor_state)
│
▼
Grafana dashboards

---

## 🛠️ Project Structure

ha_to_postgres/
│
├── .env
├── config.yaml
├── requirements.txt
├── Makefile
│
├── src/
│ ├── ha_ingest.py # MQTT → Postgres ingestion
│ ├── pipeline.py # Legacy ingestion (cron-based)
│ ├── config_loader.py # YAML config loader
│ ├── logging_config.py # OTEL logging + Python logging
│ ├── ha_client.py # Home Assistant REST client
│ ├── db.py # Postgres connection pool + inserts
│ ├── models.py # Pydantic models for validation
│ └── utils.py # Shared helpers
│
└── docs/
├── architecture.png
├── lineage_overview.md
└── roadmap.md

---

## 🔧 Setup

### 1. Clone the repository
```bash
git clone https://github.com/mrlanzelot/ha_to_postgres.git
cd ha_to_postgres

2. Create virtual environment
bash
Kopiera kod
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
bash
pip install -r requirements.txt


4. Configure environment

Create .env:

HA_BASE_URL=http://192.168.68.74:8123
HA_TOKEN=your_long_lived_token_here
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<postgres
POSTGRES_DB=home
MQTT_HOST=192.168.68.72

5. Configure sensors (config.yaml)

sensors:
  - entity_id: sensor.smhi_temperature
    value_attribute: state
    unit_attribute: unit_of_measurement

  - entity_id: sensor.last_perific_last_current_l1
    value_attribute: state
    unit_attribute: unit_of_measurement
▶ Run the ingestion pipeline (event-based)
bash
make run
Starts:

MQTT listener

JSON decoding

Validation (Pydantic)

DB insertion

Error handling

🗄 Database Schema
sql
CREATE TABLE sensor_raw (
    id SERIAL PRIMARY KEY,
    entity_id TEXT NOT NULL,
    metric TEXT NOT NULL,      -- state, temperature, humidity, power, etc.    
    value DOUBLE PRECISION,
    unit TEXTtime, 
    ts TIMESTAMPTZ NOT NULL,
);
📈 Grafana Integration
Once PostgreSQL is populated, Grafana can visualize:

Real-time sensor telemetry

EV charger load & 3-phase distribution

Weather patterns

Energy consumption

🛤 Roadmap
✔ Phase 1 (Done)
Local ingestion from MQTT

Postgres storage

YAML config

Logging 

GitHub repo creation

🔜 Phase 2 — Event-Driven Pipeline
Kafka with KRaft mode

Kafka producers & consumers

Replace MQTT → Postgres with:

nginx
Kopiera kod
HA → MQTT → Kafka → Kafka Consumer → Postgres
🔜 Phase 3 — Airflow 3 + OpenLineage
Event-triggered DAGs

Lineage tracking via OpenLineage

Dataset registration

🔜 Phase 4 — DataHub Integration
Automatic dataset and lineage publishing

Graph view of full HA-to-Grafana flow

🔜 Phase 5 — Analytics layer
Aggregated tables

Materialized views

Time-series optimizations

🧪 Tests (future)
Unit tests for ha_ingest

Integration tests via docker-compose

Kafka stream tests

📫 Contact / Author
Martin Lanzén
Home automation, data engineering, and modern pipeline enthusiast.
