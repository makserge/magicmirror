from respeaker.bing_speech_api import BingSpeechAPI as Bing
import wave
from mic_array import MicArray
import Queue
from respeaker.pixel_ring import pixel_ring
import sys
import numpy as np
import collections
from snowboydetect import SnowboyDetect
import paho.mqtt.client as mqtt

clientName = "Snowboy"
serverAddress = "192.168.31.103"

# write your Bing key here

KEY = "*****"
bing = Bing(key=KEY)

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

detector = SnowboyDetect('resources/common.res', 'resources/smart_mirror.umdl')
detector.SetAudioGain(1)
detector.SetSensitivity('0.5')

# about 5seconds
q = Queue.Queue(maxsize=768)

mqttClient = mqtt.Client(clientName)
#mqttClient.connect(serverAddress)


def gen_queue(q):
    try:
        data = q.get(timeout=1)
        while data:
            yield data
            data = q.get(timeout=1)
    except Queue.Empty:
        pass

def sendKitchenLamp(state=0): 
    if state == 1:
        send_state = "{'type': 'kitchen_lamp', 'state': '1'}"
    else:
        send_state = "{'type': 'kitchen_lamp', 'state': '0'}"
    
    print send_state
    mqttClient.publish("snowboy/command", send_state)


def main():
    history = collections.deque(maxlen=int(DOA_FRAMES / KWS_FRAMES))
    global q

    try:
        with MicArray(RATE, CHANNELS, RATE * KWS_FRAMES / 1000)  as mic:
            for chunk in mic.read_chunks():
                history.append(chunk)
                # Detect keyword from channel 0
                ans = detector.RunDetection(chunk[0::CHANNELS].tostring())
                if ans > 0:
                    print("wake up")
                    print("start recording")
                    pixel_ring.arc(12)
                    q.queue.clear()
                    for chunk in mic.read_chunks():
                        q.put(chunk[0::CHANNELS].tostring())
                        if q.full():
                            break
                    print "queue full"
                    pixel_ring.spin()
                    try:
                        text = bing.recognize(gen_queue(q))   # data can be generator
                        if text:
                            print('{}'.format(text))
                            if 'lamp on' in text:
                                sendKitchenLamp(1)
                            if 'lamp off' in text:
                                sendKitchenLamp(0)
                    except respeaker.bing_speech_api.RequestError:
                        pass
                    pixel_ring.off()

    except KeyboardInterrupt:
        pass

    pixel_ring.off()


if __name__ == '__main__':
    main()
