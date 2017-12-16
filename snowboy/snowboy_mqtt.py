#!/usr/bin/env python
# -*- coding: utf-8 -*-
import snowboydecoder
import sys
import signal
import paho.mqtt.client as mqtt

clientName = "Snowboy"
serverAddress = "192.168.31.103"

#models = ["resources/weather.pmdl", 
#		  "resources/light_on.pmdl",
#		  "resources/light_off.pmdl"
#		 ]
models = ["resources/snowboy.umdl","resources/smart_mirror.umdl"]

interrupted = False

def weatherCallback():
	print("Smart mirror!")
	#snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
	#mqttClient.publish("snowboy/hotword", "{'keyword': 'weather'}")
	
def lightOnCallback():
	print("Jarvis")
	#snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
	#mqttClient.publish("snowboy/hotword", "{'keyword': 'light_on'}")

def lightOffCallback():
	print("Snowboy")
	#snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
	#mqttClient.publish("snowboy/hotword", "{'keyword': 'light_off'}")	
	
def connectionStatus(client, userdata, flags, rc):
	print("Connected ot MQTT broker...")

def onPublish(client, userdata, result):
	print("data published with result")
	print(result)

def signalHandler(signal, frame):
    global interrupted
    interrupted = True

def interruptCallback():
    global interrupted
    return interrupted
	
#mqttClient = mqtt.Client(clientName)

#mqttClient.on_connect = connectionStatus
#mqttClient.on_publish = onPublish

#mqttClient.connect(serverAddress)

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signalHandler)

sensitivity = 1#[0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity, audio_gain=2)
print('Listening... Press Ctrl+C to exit')

callbacks = [lightOffCallback,weatherCallback]

detector.start(detected_callback=callbacks,
               interrupt_check=interruptCallback,
               sleep_time=0.03)

detector.terminate()