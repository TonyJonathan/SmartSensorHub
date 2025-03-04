import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
import json
import threading
import logging
from mqtt_client import  influx_client, influxdb_bucket


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
        query = f'''
        from(bucket: "{influxdb_bucket}") 
        |> range(start: -1h) 
        |> filter(fn: (r) => r._measurement == "sensor_data") 
        |> last()
        '''
        tables = influx_client.query_api().query(query)

        data = {"device": None, "temperature": None, "humidity": None, "time": None}

        for table in tables:
            for record in table.records:
                if record.get_field() == "temperature":
                    data["temperature"] = record.values.get("_value")
                elif record.get_field() == "humidity":
                    data["humidity"] = record.values.get("_value")
                if data["device"] is None:
                    data["device"] = record.values.get("device")
                if data["time"] is None:
                    data["time"] = record.values.get("_time")

        if data["temperature"] is None and data["humidity"] is None:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée")

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {e}")

