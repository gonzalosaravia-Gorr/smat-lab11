import paho.mqtt.client as mqtt
import requests
import json
import sys
import time

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "fisi/smat/estaciones/+/lecturas"

API_URL = "http://127.0.0.1:8000/lecturas/"

JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9maXNpIiwiZXhwIjoxNzgxMTA2NzgyfQ.0AblWk1Ak-NfPznqMlftpjOg-mEfgDvFHkxEe_v2D6s"

ultimo_valor = {}
ultimo_envio = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al Broker MQTT")
        client.subscribe(MQTT_TOPIC)
        print(f"Escuchando: {MQTT_TOPIC}")
    else:
        print(f"Error de conexión MQTT: {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    try:
        payload_raw = msg.payload.decode("utf-8")
        data_json = json.loads(payload_raw)

        topic_parts = msg.topic.split("/")
        estacion_id = int(topic_parts[3])

        valor_actual = float(data_json["valor"])

        ahora = time.time()

        if estacion_id in ultimo_valor:

            diferencia = abs(
                valor_actual - ultimo_valor[estacion_id]
            )

            tiempo = ahora - ultimo_envio[estacion_id]

            if diferencia <= 1 and tiempo < 60:
                print(
                    f"[FILTRADO] Estación {estacion_id}: {valor_actual}"
                )
                return

        api_payload = {
            "valor": valor_actual,
            "estacion_id": estacion_id
        }

        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            API_URL,
            json=api_payload,
            headers=headers
        )

        if response.status_code in [200, 201]:

            ultimo_valor[estacion_id] = valor_actual
            ultimo_envio[estacion_id] = ahora

            print(
                f"[GUARDADO] Estación {estacion_id}: {valor_actual}"
            )

        else:

            print(
                f"[ERROR API] {response.status_code}"
            )

    except Exception as e:
        print("Error:", e)

bridge_client = mqtt.Client()

bridge_client.on_connect = on_connect
bridge_client.on_message = on_message

print("Inicializando Bridge...")

bridge_client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

bridge_client.loop_forever()