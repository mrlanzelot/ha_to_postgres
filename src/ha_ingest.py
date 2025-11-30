import os
import json
import logging
import paho.mqtt.client as mqtt
import psycopg
from dotenv import load_dotenv

try:
    from src.logging_config import setup_logging
except Exception:
    from logging_config import setup_logging

setup_logging(app_name = "__name__", level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv("config/.env")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        logger.debug(f"Received MQTT message: {msg.topic}, {payload}")

        host = os.getenv("PG_HOST")
        port = int(os.getenv("PG_PORT"))
        dbname = os.getenv("PG_DB")
        user = os.getenv("PG_USER")
        password = os.getenv("PG_PASSWORD")

        # Use explicit keyword args to avoid quoting issues in f-strings
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )

        with conn:
            with conn.cursor() as cur:
                cur.execute(
            """
            INSERT INTO sensor_raw (sensor_id, metric, value, unit, ts)
            VALUES (%s, %s, %s, %s, %s)
            """,
                    (data.get("entity_id"), data.get("attribute"), data.get("state"), data.get("unit"), data.get("time")),
        )
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode MQTT payload, topic: {msg.topic}, payload: {payload}, error: {str(e)}")
    except Exception:
        logger.exception("Error processing MQTT message")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        topic = os.getenv("MQTT_TOPIC")
        logger.info("Connected to MQTT broker successfully")
        client.subscribe(topic)
        logger.info(f"Subscribed to {topic}")
    else:
        logger.error(f"Failed to connect, reason_code={reason_code}")


def on_disconnect(client, userdata, rc):
    logger.warning("MQTT disconnected", extra={"rc": rc})


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASSWORD"))
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT")))

topic = os.getenv("MQTT_TOPIC")
client.subscribe(topic)
logger.info(f"Starting MQTT loop and subscribed to {topic}")

client.loop_forever()
