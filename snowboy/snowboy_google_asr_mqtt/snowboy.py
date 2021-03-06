import snowboydecoder
import sys
import signal
import os
import paho.mqtt.client as mqtt
import speech_recognition as sr
import time
from respeaker import pixel_ring

googleAsrLanguage = "ru-RU"

mqttClientName = "ASR"
mqttBrokerHost = "192.168.31.109"
mqttBrokerLogin = ""
mqttBrokerPassword = ""

#Add your custom models here
models = ['/home/snowboy/snowboy_google_asr_mqtt/resources/smart_mirror.umdl']

waitColor = 0x0000FF
listenColor = 0x00FF00
errorColor = 0xFF0000
errorColotTimeout = 3

interrupted = False

#with open(r"/root/snowboy_google_asr_mqtt/ReSpeaker-1bbb9ef10388.json", "r") as f:
#    credentials_json = f.read()

def signalHandler(signal, frame):
    global interrupted
    interrupted = True
    pixel_ring.off()


def interruptCallback():
    global interrupted
    return interrupted

def detectedCallback():
    sys.stdout.write("recording audio...")
    sys.stdout.flush()		
    pixel_ring.set_color(rgb = listenColor)


def audioRecorderCallback(fname):
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    print "converting audio to text"
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #print(r.recognize_google_cloud(audio, language="ru-RU", credentials_json=credentials_json))
        pixel_ring.wait()
        result = r.recognize_google(audio, language = googleAsrLanguage)
        mqttClient.publish("asr/command", result)
        print result
        pixel_ring.set_color(rgb = waitColor)
    except sr.UnknownValueError:
        print "Google Speech Recognition could not understand audio"
        pixel_ring.set_color(rgb = errorColor)
        time.sleep(errorColotTimeout)
        pixel_ring.set_color(rgb = waitColor)
    except sr.RequestError as e:
        print "Could not request results from Google Speech Recognition service; {0}".format(e)
        pixel_ring.set_color(rgb = errorColor)
        time.sleep(errorColotTimeout)
        pixel_ring.set_color(rgb = waitColor)
        
    os.remove(fname)
	
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signalHandler)

mqttClient = mqtt.Client(mqttClientName)
#mqttClient.username_pw_set(mqttBrokerLogin, mqttBrokerPassword)
mqttClient.connect(mqttBrokerHost)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity = sensitivity)
print('Listening... Press Ctrl+C to exit')

pixel_ring.set_color(rgb = waitColor)

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback = detectedCallback,
               audio_recorder_callback = audioRecorderCallback,
               interrupt_check = interruptCallback,
               sleep_time = 0.03)

detector.terminate()
