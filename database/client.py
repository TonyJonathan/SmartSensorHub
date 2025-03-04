from influxdb_client import InfluxDBClient, WriteApi, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialise le client InfluxDB
influxdb_client = InfluxDBClient(url="http://localhost:8086", token="LiahQVPt9eklAQO_DZxIwxGmPdhXypgtg576i08-MEdGJ79xtEmOrqh0EYOe4U3-H0-MuZ8_hnjrcpijM7ONhw==", org="SmartSensorHub")

# Initialise l'API d'écriture avec les options appropriées
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
