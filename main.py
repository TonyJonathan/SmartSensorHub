import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
from influxdb_client import InfluxDBClient, Point, WritePrecision
import json
import threading
import logging

# Configuration InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "LiahQVPt9eklAQO_DZxIwxGmPdhXypgtg576i08-MEdGJ79xtEmOrqh0EYOe4U3-H0-MuZ8_hnjrcpijM7ONhw=="
influxdb_org = "SmartSensorHub"
influxdb_bucket = "my_data"

# Initialisation du client InfluxDB
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influx_client.write_api(write_options=WritePrecision.NS)

# Configuration du client MQTT
mqtt_broker = "localhost"
mqtt_port = 1884
mqtt_topic = "sensor/data"

# Initialisation du client MQTT
client = mqtt.Client()

# Fonction de traitement des messages MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        point = Point("sensor_data") \
            .tag("device", data.get("device", "unknown")) \
            .field("temperature", data.get("temperature", None)) \
            .field("humidity", data.get("humidity", None))
        write_api.write(bucket=influxdb_bucket, record=point)
        logging.info(f"Message traité et écrit dans InfluxDB: {data}")
    except Exception as e:
        logging.error(f"Erreur lors du traitement du message: {e}")

client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)
client.subscribe(mqtt_topic)

# Fonction pour faire tourner la boucle MQTT dans un thread séparé
def mqtt_loop():
    client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

# Initialisation de FastAPI
app = FastAPI()

# Endpoint pour la page d'accueil
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur SmartSensor Hub!"}

# Endpoint pour récupérer les dernières données de température et d'humidité
@app.get("/data/latest")
def get_latest_data():
    try:
        query = f'from(bucket: "{influxdb_bucket}") |> range(start: -1h) |> last()'
        tables = influx_client.query_api().query(query)
        if tables:
            for record in tables[0].records:
                return {
                    "device": record.values.get("device"),
                    "temperature": record.values.get("temperature"),
                    "humidity": record.values.get("humidity"),
                    "time": record.values.get("_time")
                }
        else:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {e}")
