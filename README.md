# SensoryData
Repository for Edge and Server program

Overview
-----------------
2 files created, one for running on edge devices- **edge_publisher** and the other one is for server- **edge_server**

Description
-----------------
**edge_publisher**
-Reads each data point from dataset.csv after every 60-sec delay and publish to the cloud(live data)
-If the server returns failure or server is stopped the data point is buffered locally as dequeue.
-Publish all the buffered data after every 5 seconds.
-Prints count of packets sent and buffered.

**edge_server**
 -Implements a MQTT broker which accepts data
 -Provides success or failure for the received data
 -And each new data is appended to a dataset_output.csv file

Technologies Used
-----------------
-MQTT Broker used - Mosquitto Broker, which is running on localhost and port 1833.
-Python v3.8.0
-Eclipse IDE
