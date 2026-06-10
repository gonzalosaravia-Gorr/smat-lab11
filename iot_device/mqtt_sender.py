import paho.mqtt.client as mqtt
import time
import json
import random

broker = "broker.hivemq.com"
port = 1883
topic = "fisi/smat/estaciones/1/lecturas"

client = mqtt.Client()
client.connect(broker, port, 60)

value = 50.0

while True:
    value += random.uniform(-0.3, 0.3)

    payload = {
        "valor": round(value, 2)
    }

    client.publish(topic, json.dumps(payload))

    print(f"📤 Enviado: {payload}")

    time.sleep(1)