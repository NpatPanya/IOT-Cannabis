# python 3.6import random
import time
import random
import json
# import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client


import multiprocessing
print("Number of cpu : ", multiprocessing.cpu_count())

broker = 'm15.cloudmqtt.com'
port = 12987
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'cyejnmdr'
password = 'Is7roaqnQX09'

# Define GPIO pins for sensors
# TEMP_PIN = 17
# HUMIDITY_PIN = 18
# EC_PIN = 19
# PH_PIN = 20
# N_PIN = 21
# P_PIN = 22
# K_PIN = 23
# PUMP_PIN = 24
# SPRAY_PIN = 25
# FERTILIZER_PIN = 26
  
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
    #collect senssor data to variable
    # tempsensor = GPIO?
    # humidity_sensor = GPIO?
    # EC_sensor = GPIO?
    # PH_sensor = GPIO?
    # N_meter = GPIO? 
    # P_meter = GPIO? 
    # K_meter = GPIO?

    msg_count = 0
    while True:
        time.sleep(3)
        topic="tttt"
        msg = f"{msg_count+1},{msg_count+2},{msg_count+3},{msg_count+4},{msg_count+5},{msg_count+6},{msg_count+7}"
        # msg = f"{humidity_sensor},{temperature},{EC_sensor},{PH_sensor},{N_meter},{P_meter},{K_meter}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        print(msg)
        if msg_count==100:
           msg_count =0
        else:
           msg_count+=1

pump = None
spray = None
med = None
Ipump = None
Ispray = None
Ifertilizer = None

def subscribe(client: mqtt_client):
    client.subscribe("testsenddevicestatus")
    client.subscribe("testsenddeviceInterval")
    # client.subscribe("wbutton_com")
    # client.subscribe("sbutton_com")
    # client.subscribe("fbutton_com")
    # client.subscribe("lbutton_com")
    client.on_message = on_message #"waterpump,on" "waterpump,off","medpump,on"
    
def on_message(client, userdata, msg):
    
    # print(f"Received device: {device}, Status: {status}")
    if msg.topic == "testsenddevicestatus":
        message = msg.payload.decode("utf-8")  # Parse the JSON payload
        print(message)
        payload = json.loads(message)
        device = payload["device"]  # Extract the value of the "device" key
        status = payload["state"] # Extract the value of the "status" key
        # print(device," : ",status)
        if device == "waterpump":
            pump = status
            print(device,pump)

        elif device == "bugkiller":
            spray = status
            print(device,spray)

        elif device == "fertilizer":
            fertilizer = status
            print (device,fertilizer)

        elif device == "Light":
            light_bulb = status
            print (device,light_bulb)
            
    elif msg.topic == "testsenddeviceInterval":
        message =msg.payload.decode("utf-8") # Parse the JSON payload
        print(message)
        payload = json.loads(message)
        Idevice = payload["type"]  # Extract the value of the "device" key
        Interval = payload["Interval"] # Extract the value of the "status" key
        # print(Idevice," : ",Interval)
        if Idevice == "WaterPump":
            Ipump = int(Interval)
            print(type(Ipump))
            print(Idevice,Ipump)

        if Idevice == "Spray":
            Ispray = int(Interval)
            print(type(Ispray))
            print(Idevice,Ispray)

        if Idevice == "Fertilizer":
            Ifertilizer = int(Interval)
            print(type(Ifertilizer ))
            print(Idevice,Ifertilizer )

        if Idevice == "Light":
            ILight = int(Interval)
            print(type(ILight ))
            print(Idevice,ILight )

    # elif msg.topic == "wbutton_com":
    #     payload = json.loads(msg.payload.decode())  # Parse the JSON payload
    #     wdevice = payload.get('device')  # Extract the value of the "device" key
    #     wstatus = payload.get('state') # Extract the value of the "status" key
    #     print (wstatus)
    #     if wdevice == "waterpump":
    #         if wstatus == "On":
    #             print(wdevice,wstatus)
    #         else:
    #             print(wdevice,wstatus)

    # elif msg.topic == "sbutton_com":
    #     payload = json.loads(msg.payload.decode())  # Parse the JSON payload
    #     sdevice = payload.get('device')  # Extract the value of the "device" key
    #     sstatus = payload.get('state') # Extract the value of the "status" key
    #     print (sstatus)
    #     if sdevice == "bugkiller":
    #         if sstatus == "On":
    #             print(sdevice,sstatus)
    #         else:
    #             print(sdevice,sstatus)

    # elif msg.topic == "fbutton_com":
    #     payload = json.loads(msg.payload.decode())  # Parse the JSON payload
    #     fdevice = payload.get('device')  # Extract the value of the "device" key
    #     fstatus = payload.get('state') # Extract the value of the "status" key
    #     print (fstatus)
    #     if fdevice == "fertilizer":
    #         if fstatus == "On":
    #             print(fdevice,fstatus)
    #         else:
    #             print(fdevice,fstatus)

    # elif msg.topic == "lbutton_com":
    #     payload = json.loads(msg.payload.decode())  # Parse the JSON payload
    #     ldevice = payload.get('device')  # Extract the value of the "device" key
    #     lstatus = payload.get('state') # Extract the value of the "status" key
    #     print (lstatus)
    #     if ldevice == "Light":
    #         if lstatus == "On":
    #             print(ldevice,lstatus)
    #         else:
    #             print(ldevice,lstatus)
                    
        
def publish_pro1(client):
    publish(client)
    
def subscribe_pro2(client):
    subscribe(client)
    client.loop_forever()
    

    
def run():
    
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
   
    print("Done!") 
    
    
if __name__ == '__main__':
    run()
