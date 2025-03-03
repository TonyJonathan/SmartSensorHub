import paho.mqtt.client as mqtt
from fastapi import FastAPI
from mqtt_client import mqtt_client
from database.client import write_api
from mqtt_client import mqtt_thread


app = FastAPI()

# Configuration du client MQTT
mqtt_broker = "localhost"  # Adresse de ton broker (localhost si Mosquitto est installé localement)
mqtt_port = 1884
mqtt_topic = "sensor/data"  # Le topic auquel les capteurs enverront les données

# Fonction pour traiter les messages MQTT reçus
def on_message(client, userdata, msg):
    print(f"Message reçu : {msg.payload.decode()}")
    # Tu peux ici traiter le message et l'ajouter à la base de données InfluxDB
    # Par exemple, on va simplement l'afficher ici pour commencer.

# Configurer le client MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port)

# S'abonner au topic
client.subscribe(mqtt_topic)

# Démarrer le client MQTT dans un thread séparé
import threading

def mqtt_loop():
    client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()

@app.get("/")
def read_root():
    return {"message": "Welcome to SmartSensor Hub!"}
