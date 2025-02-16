#module to set up HiveMQ MQTTQ service
import network
from WIFI_CONFIG import * # you will need to create a module with this name that contains your wifi SSID and PASSWORD as variables
from hive_credentials import * ##you will need to create a module with this name and add HIVE_CLIENT_ID,HIVE_SERVER_ID, HIVE_USER, HIVE_PASSWORD as byte literals useing syntax variable_name = b"[your string here]"
from umqtt.simple import MQTTClient
import random
from time import sleep, sleep_ms
import ssl
from ntptime import settime
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)
settime()
print(time.localtime())

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_NONE

def connectMQTT():
    client = MQTTClient(client_id=HIVE_CLIENT_ID,
        server=HIVE_SERVER_ID,
        port=0,
        user=HIVE_USER,
        password=HIVE_PASSWORD,
        keepalive=7200,
        ssl= context)

    client.connect()
    return client

#client = connectMQTT()

def publish(client,topic, value):
    print(topic)
    print(value)
    client.publish(topic,value)
    print("PUBLISH COMPLETE")
  
