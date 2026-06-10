import paho.mqtt.client as mqtt
import requests
import json
import sys
import time

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "fisi/smat/estaciones/+/lecturas"

API_URL = "http://127.0.0.1:8000/lecturas/"

JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl9maXNpIiwiZXhwIjoxNzgxMTA5NTc5fQ.q_Wve3FZX1-4ihsxeF6aZrPEyX3wWieLXUafEFjG0N8"

# Cache de último valor guardado por estación
cache = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("🟢 Conectado al Broker MQTT")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Escuchando: {MQTT_TOPIC}")
    else:
        print(f"🔴 Error de conexión: {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    try:
        payload_raw = msg.payload.decode("utf-8")
        data_json = json.loads(payload_raw)

        topic_parts = msg.topic.split("/")
        estacion_id = int(topic_parts[3])

        valor = float(data_json["valor"])

        ahora = time.time()

        print(f"📩 Recibido -> Estación {estacion_id} | Valor {valor}")

        # Primera lectura
        if estacion_id not in cache:

            cache[estacion_id] = {
                "valor": valor,
                "timestamp": ahora
            }

            print("🆕 Primera lectura de la estación")
            enviar_api(estacion_id, valor)
            return

        ultimo_valor = cache[estacion_id]["valor"]
        ultimo_tiempo = cache[estacion_id]["timestamp"]

        variacion = abs(valor - ultimo_valor)

        if ultimo_valor == 0:
            porcentaje = 100
        else:
            porcentaje = (variacion / abs(ultimo_valor)) * 100

        tiempo_transcurrido = ahora - ultimo_tiempo

        if porcentaje > 5 or tiempo_transcurrido > 60:

            cache[estacion_id]["valor"] = valor
            cache[estacion_id]["timestamp"] = ahora

            motivo = []

            if porcentaje > 5:
                motivo.append(f"cambio {porcentaje:.2f}%")

            if tiempo_transcurrido > 60:
                motivo.append("timeout 60s")

            print(f"✅ Aceptado -> {', '.join(motivo)}")

            enviar_api(estacion_id, valor)

        else:

            print(
                f"🚫 FILTRADO -> "
                f"Estación {estacion_id} | "
                f"Valor {valor} | "
                f"Cambio {porcentaje:.2f}% | "
                f"{tiempo_transcurrido:.0f}s"
            )

    except Exception as e:
        print(f"❌ Error: {e}")

def enviar_api(estacion_id, valor):

    api_payload = {
        "valor": valor,
        "estacion_id": estacion_id
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JWT_TOKEN}"
    }

    try:

        response = requests.post(
            API_URL,
            json=api_payload,
            headers=headers,
            timeout=10
        )

        if response.status_code in [200, 201]:

            print(
                f"💾 Guardado -> "
                f"Estación {estacion_id} | "
                f"Valor {valor}"
            )

        else:

            print(
                f"⚠️ API rechazó dato -> "
                f"{response.status_code} {response.text}"
            )

    except Exception as e:
        print(f"❌ Error HTTP: {e}")

bridge_client = mqtt.Client()

bridge_client.on_connect = on_connect
bridge_client.on_message = on_message

try:

    print("🚀 Iniciando Bridge SMAT...")

    bridge_client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    bridge_client.loop_forever()

except KeyboardInterrupt:

    print("\n🛑 Bridge detenido")