SMAT - Laboratorio 11: Ingesta de Telemetría (MQTT → HTTP)

Descripcion

Este proyecto implementa un sistema de comunicacion IoT donde los datos de telemetria enviados por dispositivos MQTT son recibidos por un bridge en Python y luego reenviados a un backend HTTP.

El objetivo es simular un ecosistema completo de ingesta de datos en tiempo real, integrando protocolos ligeros MQTT con servicios web HTTP REST.

Arquitectura del sistema

mqtt_sender.py → simula el dispositivo IoT que envia datos por MQTT
mqtt_bridge.py → recibe mensajes MQTT y los transforma a formato HTTP
Backend HTTP → recibe y procesa los datos de telemetria
Broker MQTT → intermediario de mensajeria como Mosquitto

Tecnologias usadas

Python 3
MQTT paho-mqtt
HTTP Requests requests library
Git GitHub
Mosquitto Broker

Flujo de ejecucion

1. Se inicia el broker MQTT Mosquitto
2. Se ejecuta el backend HTTP
3. Se ejecuta mqtt_bridge.py que escucha MQTT
4. Se ejecuta mqtt_sender.py que envia datos
5. El bridge recibe los mensajes y los reenvia por HTTP

Estructura del proyecto

smat-ecosistema-2026
mqtt_sender.py
mqtt_bridge.py
backend
mobile
README.md

Ejecucion

1. Instalar dependencias
   pip install paho-mqtt requests

2. Ejecutar bridge
   python mqtt_bridge.py

3. Ejecutar sender
   python mqtt_sender.py

Resultado esperado

Los datos enviados por MQTT son recibidos correctamente por el bridge y enviados al backend HTTP sin perdida de informacion

Autor
Gonzalo Saravia
Proyecto academico SMAT 2026
