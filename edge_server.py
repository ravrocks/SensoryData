import paho.mqtt.client as mqtt
import time
import json
import csv
mqtt_host = "localhost"
class Sensor:
    active_instance = None
    def __init__(self, string_inp):
        tmp = string_inp.split(", ")
        self.timestamp=tmp[2]
        self.value=tmp[1]
        self.sensor_type=tmp[0]
        Sensor.active_instance = self
###############################################
def on_connect(my_client, userdata, flags, rc):
    print("Result from connect: {}".format(mqtt.connack_string(rc)))
    if rc == mqtt.CONNACK_ACCEPTED:
        my_client.subscribe("Sensory Data") #to solve recoonection probs
def on_subscribe(client, userdata, mid, granted_qos):
    print("Successfully subscribed")
def on_print_all(client, userdata, message):
    print("Successfully message received.")
    tmpz=str(message.payload.decode("utf-8")).split(", ")
    Sensor.active_instance.timestamp=tmpz[2]
    Sensor.active_instance.value=tmpz[1]
    Sensor.active_instance.sensor_type=tmpz[0]
    rows=[[Sensor.active_instance.timestamp,Sensor.active_instance.value,Sensor.active_instance.sensor_type]]
    filename = "dataset_output.csv"
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
        
##########################################################
if __name__ == "__main__":
    Sensor = Sensor(" , , ") 
    my_client = mqtt.Client("IMSERVER")
    my_client.on_message= on_print_all
    my_client.connect(host=mqtt_host, port=1883)
    my_client.on_connect = on_connect
    my_client.on_subscribe = on_subscribe
    my_client.loop_forever()