# Ignore warnings in VS Code
# type: ignore

# Pre-defined libraries
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import json
import socketpool
import ssl
import time
import wifi

# Local libraries
import secrets
from thp_sensor import ThpSensor

#################################
#          Definitions          #
#################################

# Device Details
DEVICE_ID = "aci-5x5-thermometer"
# https://www.epochconverter.com/timezones
# TIMEZONE_OFFSET_SECONDS = 21600
TIMEZONE_OFFSET_SECONDS = 18000
TIME_DELAY = 60 * 60 # one hour

# MQTT Details
BROKER_HOST="192.168.0.8"
BROKER_PORT=1883
MESSAGE_TOPIC = f"devices/{DEVICE_ID}/messages"
COMMAND_TOPIC = f"devices/{DEVICE_ID}"

def connect_to_wireless():
    wifi.radio.connect(ssid=secrets.SSID, password=secrets.PASSWORD)
    print("Connected")
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    print("My IP address is", wifi.radio.ipv4_address)


def handle_connect(client, userdata, flags, rc):
    print("Connected to broker!")
    client.subscribe(COMMAND_TOPIC)
    print(f"Subscribed to {COMMAND_TOPIC}")


def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker!")


def handle_message(client, topic, message):
    print(f"Received new message on topic {topic}: {message}")
    message_object = json.loads(message)
    message_type = message_object.get("MessageType")
    if (message_type == 1):
        global device_key
        device_key = message_object.get("Payload")
        print(f"Set device_key to {device_key}")


def configure_requests():
    global pool
    global ssl_context
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()


#################################
#             Logic             #
#################################

connect_to_wireless()
configure_requests()

sensor = ThpSensor(TIMEZONE_OFFSET_SECONDS)
mqtt_client = MQTT.MQTT(
    client_id=DEVICE_ID,
    broker=BROKER_HOST,
    port=BROKER_PORT,
    socket_pool=pool,
    ssl_context=ssl_context
)
mqtt_client.on_connect = handle_connect
mqtt_client.on_disconnect = handle_disconnect
mqtt_client.on_message = handle_message
mqtt_client.connect()

while True:
    # Poll the subscription queue
    mqtt_client.loop(timeout=1)
    
    # Read sensors and generate telemetry
    telemetry = sensor.generate_telemetry()

    if (device_key is not None):
        # Publish telemetry to broker
        message = {
            "DeviceKey": device_key,
            "Timestamp": telemetry[0].get("Timestamp"),
            "Payload": telemetry
        }
    
        mqtt_client.publish(MESSAGE_TOPIC, json.dumps(message))
        
    time.sleep(TIME_DELAY)