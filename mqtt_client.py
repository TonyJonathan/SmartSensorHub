import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions
import json
import threading

# Configuration InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "LiahQVPt9eklAQO_DZxIwxGmPdhXypgtg576i08-MEdGJ79xtEmOrqh0EYOe4U3-H0-MuZ8_hnjrcpijM7ONhw=="
influxdb_org = "SmartSensorHub"
influxdb_bucket = "my_data"

# Initialisation du client InfluxDB
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influx_client.write_api(write_options=WriteOptions())

# Configuration du client MQTT
mqtt_broker = "localhost"
mqtt_port = 1884
mqtt_topic = "sensor/data"

# Fonction de traitement des messages MQTT
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    data = json.loads(payload)
    point = Point("sensor_data") \
        .tag("device", data.get("device")) \
        .field("temperature", float(data.get("temperature"))) \
        .field("humidity", float(data.get("humidity")))
    write_api.write(bucket=influxdb_bucket, record=point)

# Initialisation du client MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.subscribe(mqtt_topic)

# Fonction pour faire tourner la boucle MQTT dans un thread séparé
def mqtt_loop():
    mqtt_client.loop_forever()

# Démarrage du thread MQTT
mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()
