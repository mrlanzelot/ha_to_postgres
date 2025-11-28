Below is a clean, minimal, beginner-friendly Python script that pulls a single sensor value from Home Assistant and stores it in PostgreSQL.
This is the perfect first step before adding Airflow, Kafka, or DataHub.

The script is short, safe, and easy to run on your Ubuntu machine.

✅ 1. Requirements (install libraries)

Run these on your Ubuntu server:

pip install requests psycopg2-binary python-dotenv

✅ 2. Create a .env file

Store your Home Assistant token and DB credentials:

HA_BASE_URL=https://mlha.lanzen.se:8123
HA_TOKEN=your_long_lived_access_token

PG_HOST=localhost
PG_PORT=5432
PG_DB=home_db
PG_USER=postgres
PG_PASSWORD=yourpassword


Generate HA token under:
Profile → Security → Long-lived access tokens

✅ 3. Create the PostgreSQL table (once)
CREATE TABLE energy_raw (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    value NUMERIC,
    unit TEXT,
    ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

✅ 4. Minimal Python Script: HA → Postgres

Save as: ha_to_postgres.py

import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Home Assistant config
HA_BASE_URL = os.getenv("HA_BASE_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# PostgreSQL config
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

# Example: read electricity consumption sensor
SENSOR_ID = "sensor.energy_consumption"


def get_sensor_value(sensor_id):
    """Fetch a single sensor state from Home Assistant."""
    url = f"{HA_BASE_URL}/api/states/{sensor_id}"

    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    value = data.get("state")
    unit = data.get("attributes", {}).get("unit_of_measurement")

    return value, unit


def write_to_postgres(sensor_id, value, unit):
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO energy_raw (sensor_id, value, unit)
        VALUES (%s, %s, %s)
        """,
        (sensor_id, value, unit),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    value, unit = get_sensor_value(SENSOR_ID)
    print(f"Fetched from HA: {value} {unit}")

    write_to_postgres(SENSOR_ID, value, unit)
    print("Written to PostgreSQL.")

✅ 5. Run it
Using the Makefile (recommended):
```
make install
make run
```
To test without writing to Postgres use DRY_RUN:
```
DRY_RUN=true make run
```

The script now writes structured logs to `logs/ha_ingest.log` and stdout. You can control verbosity with `LOG_LEVEL` (DEBUG/INFO/WARNING/ERROR).


Expected output:

Fetched from HA: 1.25 kWh
Written to PostgreSQL.


And in PostgreSQL:

SELECT * FROM energy_raw ORDER BY id DESC LIMIT 5;

🔍 How this helps you learn

This script teaches the fundamentals:

Calling the Home Assistant REST API

Parsing JSON

Inserting into PostgreSQL

Working with timestamps and units

Creating a basic ETL flow


CREATE TABLE sensor_raw (
    id SERIAL PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value NUMERIC,
    unit TEXT,
    ts TIMESTAMPTZ
);