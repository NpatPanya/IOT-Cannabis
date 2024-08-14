import random
import time
import json
from paho.mqtt import client as mqtt_client

broker = 'm15.cloudmqtt.com'
port = 12987
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'cyejnmdr'
password = 'Is7roaqnQX09'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        topic = "tttt"
        msg = f"{msg_count+1},{msg_count+2},{msg_count+3},{msg_count+4},{msg_count+5},{msg_count+6},{msg_count+7}" 
        result = client.publish(topic, msg)
        print(msg)
        if msg_count == 100:
            msg_count = 0
        else:
            msg_count += 1

def subscribe(client: mqtt_client):
    client.subscribe("testsenddevicestatus")
    client.on_message = on_message

def on_message(client, userdata, msg):
    global pump, spray, med
    payload = json.loads(msg.payload.decode())
    device = payload["device"]
    status = payload["status"]
    if device == "waterpump":
        pump = status
        print(device, pump)
    elif device == "bugkiller":
        spray = status
        print(device, spray)
    elif device == "fertilizer":
        med = status
        print(device, med)

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    subscribe(client)

if __name__ == '__main__':
    run()
