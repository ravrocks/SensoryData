import paho.mqtt.client as mqtt
import time
import csv
import string
from collections import deque
from asyncio.tasks import sleep

#########################################################################
def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(mqtt.connack_string(rc)))
    if rc != mqtt.CONNACK_ACCEPTED:
        raise IOError("Couldn't establish a connection with the MQTT server")
    client.subscribe("Sensory Data", qos=0)
    retry_Send()
            
    
def publish_value(client, topic, value):
    result = client.publish(topic=topic, payload=value, qos=0)
    return result

def on_message(client, userdata, msg):
    print("message received " ,str(msg.payload.decode("utf-8")))
    
def retry_Send():
    global qstruct
    if len(qstruct)!=0:
        qstruct2 = deque()
        qstruct2=qstruct
        while len(qstruct2)!=0:
            tmp=qstruct2.popleft()
            result=publish_value(client, "Sensory Data" ,tmp)
            time.sleep(5)
            if result[0]==0:
                continue;
            else:
                print("Big probs!")
                qstruct=qstruct2
                break;
##########################################################################
if __name__ == "__main__":
    qstruct = deque()
    client = mqtt.Client("CLient1")
    client.on_connect = on_connect
    client.on_message=on_message
    client.connect(host="localhost", port=1883)
    client.loop_start()
    print_me = "{}, {}, {}"
   
    while True:
        with open('dataset.csv') as csvfile:
            reader=csv.reader(csvfile)
            fline = True
            for row in reader:
                if fline:    #skipping first for header
                    fline = False
                    continue
                timestamp = str(row[0])
                valz = float(row[1])
                sensor_type= str(row[2])
                print(print_me.format(sensor_type, valz,timestamp))
                resultxx=publish_value(client, "Sensory Data" ,print_me.format(sensor_type, valz,timestamp))
                if resultxx[0] != 0:
                    qstruct.append(print_me.format(sensor_type, valz,timestamp))
                time.sleep(60)
 
    client.disconnect()
    client.loop_stop()