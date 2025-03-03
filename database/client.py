from influxdb_client import InfluxDBClient, WriteApi, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Initialise le client InfluxDB
influxdb_client = InfluxDBClient(url="http://localhost:8086", token="ton_token", org="ton_organisation")

# Initialise l'API d'écriture avec les options appropriées
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
