#--------------------------------------------------------#
# python 3.6import random
import time
import random
import json
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client


import multiprocessing
print("Number of cpu : ", multiprocessing.cpu_count())

broker = 'm15.cloudmqtt.com'
port = 12987
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'cyejnmdr'
password = 'Is7roaqnQX09'

# Define GPIO pins for sensors
TEMP_PIN = 17
HUMIDITY_PIN = 18
EC_PIN = 19
PH_PIN = 20
N_PIN = 21
P_PIN = 22
K_PIN = 23
PUMP_PIN = 24
SPRAY_PIN = 25
FERTILIZER_PIN = 26
  
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def publish(client):
    msg_count = 0
    while True:
        time.sleep(3)
        topic="tttt"
        msg = f"{GPIO.input(HUMIDITY_PIN)},{GPIO.input(TEMP_PIN)},{GPIO.input(EC_PIN)},{GPIO.input(PH_PIN)},{GPIO.input(N_PIN)},{GPIO.input(P_PIN)},{GPIO.input(K_PIN)}"
        # msg = f"{tempsensor},{humidity_sensor},{EC_sensor},{PH_sensor},{N_meter},{P_meter},{K_meter}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        print(msg)
        if msg_count==100:
           msg_count =0
        else:
           msg_count+=1


def subscribe(client: mqtt_client):
    client.subscribe("testsenddevicestatus")
    client.subscribe("testsenddeviceInterval")
    client.subscribe("wbutton_com")
    client.subscribe("sbutton_com")
    client.subscribe("fbutton_com")
    client.on_message = on_message #"waterpump,on" "waterpump,off","medpump,on"
    
def on_message(client, userdata, msg):
    
    # print(f"Received device: {device}, Status: {status}")
    if msg.topic == "testsenddevicestatus":
        payload = json.loads(msg.payload.decode())  # Parse the JSON payload
        device = payload.get('device')  # Extract the value of the "device" key
        status = payload.get('state') # Extract the value of the "status" key
        if device == "waterpump":
            pump = status
            if pump == "On":
                GPIO.output(PUMP_PIN, GPIO.HIGH)
            else :
                GPIO.output(PUMP_PIN, GPIO.LOW)
            print(device,pump)

        elif device == "bugkiller":
            spray = status
            if spray == "On":
                GPIO.output(SPRAY_PIN, GPIO.HIGH)
            else :
                GPIO.output(SPRAY_PIN, GPIO.LOW)
            print(device,spray)

        elif device == "fertilizer":
            fertilizer = status
            if fertilizer == "On":
                GPIO.output(FERTILIZER_PIN,GPIO.HIGH)
            else:
                GPIO.output(FERTILIZER_PIN,GPIO.LOW)
            print (device,fertilizer)
            
    elif msg.topic == "testsenddeviceInterval":
        payload = json.loads(msg.payload.decode())  # Parse the JSON payload
        Idevice = payload.get('type')  # Extract the value of the "device" key
        Interval = payload.get('Interval') # Extract the value of the "status" key
        if Idevice == "WaterPump":
            Ipump = int(Interval)
            for i in range(Ipump,-1,-1):
                if i == 0:
                    GPIO.output(PUMP_PIN,GPIO.LOW)
                    break
            print(Idevice,Ipump)

        if Idevice == "Spray":
            Ispray = int(Interval)
            for i in range(Ispray,-1,-1):
                if i == 0:
                    GPIO.output(SPRAY_PIN,GPIO.LOW)
                    break
            print(Idevice,Ispray)

        if Idevice == "Fertilizer":
            Ifertilizer = int(Interval)
            for i in range(Ifertilizer,-1,-1):
                if i == 0:
                    GPIO.output(FERTILIZER_PIN,GPIO.LOW)
                    break
            print(Idevice,Ifertilizer)

    elif msg.topic == "wbutton_com":
        payload = json.loads(msg.payload.decode())  # Parse the JSON payload
        wdevice = payload.get('device')  # Extract the value of the "device" key
        wstatus = payload.get('state') # Extract the value of the "status" key
        # print (wstatus)
        if wdevice == "waterpump":
            if wstatus == "On":
                GPIO.output(PUMP_PIN,GPIO.HIGH)
            elif wstatus == "Off":
                GPIO.output(PUMP_PIN,GPIO.LOW)

    elif msg.topic == "sbutton_com":
        payload = json.loads(msg.payload.decode())  # Parse the JSON payload
        sdevice = payload.get('device')  # Extract the value of the "device" key
        sstatus = payload.get('state') # Extract the value of the "status" key
        # print (sstatus)
        if sdevice == "bugkiller":
            if sstatus == "On":
                GPIO.output(SPRAY_PIN,GPIO.HIGH)
            elif sstatus == "Off":
                GPIO.output(SPRAY_PIN,GPIO.LOW)

    elif msg.topic == "fbutton_com":
        payload = json.loads(msg.payload.decode())  # Parse the JSON payload
        fdevice = payload.get('device')  # Extract the value of the "device" key
        fstatus = payload.get('state') # Extract the value of the "status" key
        # print (fstatus)
        if fdevice == "fertilizer":
            if fstatus == "On":
                GPIO.output(FERTILIZER_PIN,GPIO.HIGH)
            elif fstatus == "Off":
                GPIO.output(FERTILIZER_PIN,GPIO.LOW)
        
def publish_pro1(client):
    publish(client)
    
def subscribe_pro2(client):
    subscribe(client)
    client.loop_forever()
    

    
def run():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([PUMP_PIN, SPRAY_PIN, FERTILIZER_PIN], GPIO.OUT)
    GPIO.setup([TEMP_PIN, HUMIDITY_PIN, EC_PIN, PH_PIN, N_PIN, P_PIN, K_PIN], GPIO.IN)
    
    
    client = connect_mqtt()
        
    p1 = multiprocessing.Process(target=publish_pro1,args=(client,)) 
    p2 = multiprocessing.Process(target=subscribe_pro2,args=(client,)) 
  
    # starting process 1 
    p1.start() 
    # starting process 2 
    p2.start() 
  
    # wait until process 1 is finished 
    p1.join() 
    # wait until process 2 is finished 
    p2.join() 
  
    # both processes finished 
    GPIO.cleanup()
    print("Done!") 
    
    
if __name__ == '__main__':
    run()
