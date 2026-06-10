import paho.mqtt.client as mqtt
import json
import random
import time

BROKER = "broker.hivemq.com"
TOPIC = "fisi/smat/estaciones/1/lecturas"

client = mqtt.Client()

client.connect(
    BROKER,
    1883,
    60
)

while True:

    valor = round(
        random.uniform(40, 50),
        2
    )

    payload = {
        "valor": valor
    }

    client.publish(
        TOPIC,
        json.dumps(payload)
    )

    print("Enviado:", payload)

    time.sleep(5)