#!/usr/bin/env python
# -*- coding: utf-8 -*-
import snowboydecoder
import sys
import wave
import paho.mqtt.client as mqtt

clientName = "Snowboy"
serverAddress = "192.168.31.103"

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/gpio")

def messageDecoder(client, userdata, msg):
	message = msg.payload.decode(encoding='UTF-8')
	
	if message == "on":
		print("LED is ON!")
	elif message == "off":
		print("LED is OFF!")
	else:
		print("Unknown message!")
		
def onPublish(client, userdata, result):
	print("data published \n")
	print("\nresult:")
	print(result)
	
	
mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder
mqttClient.on_publish = onPublish

mqttClient.connect(serverAddress)
print("Connected...")

mqttClient.publish("house/bulb1", "on")

#mqttClient.loop_forever()