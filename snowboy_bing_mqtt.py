from respeaker.bing_speech_api import BingSpeechAPI as Bing
import wave
from mic_array import MicArray
import Queue
from pixel_ring import pixel_ring
import sys
import numpy as np
import collections
from snowboydetect import SnowboyDetect
import time
import json
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError

# write your Wio token here

WIO_TOKEN = "**************"

# write your Bing key here

KEY = "**********"
bing = Bing(key=KEY)

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

detector = SnowboyDetect('snowboy/resources/common.res', 'snowboy/resources/snowboy.umdl')
detector.SetAudioGain(1)
detector.SetSensitivity('0.5')

# about 5seconds
q = Queue.Queue(maxsize=768)

def gen_queue(q):
    try:
        data = q.get(timeout=1)
        while data:
            yield data
            data = q.get(timeout=1)
    except Queue.Empty:
        pass

def controlLED(onoff=0): 
    try:
        if onoff == 1:
            rgb_hex_string = '000080'
        else:
            rgb_hex_string = '000000'
        url = 'https://cn.wio.seeed.io/v1/node/GroveLedWs2812D0/clear/4/{}?access_token={}'.format(rgb_hex_string, WIO_TOKEN)
        request = Request(url, data='')
        response = urlopen(request)
        data = response.read()
        result = json.loads(data)
        if result['result'] == 'ok':
            return True
        else:
            return False
    except Exception as err:
        return False

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
                    text = bing.recognize(gen_queue(q))   # data can be generator
                    if text:
                        print('{}'.format(text))
                        if 'turn on' in text:
                            controlLED(1)
                        if 'turn off' in text:
                            controlLED(0)
                    pixel_ring.off()

    except KeyboardInterrupt:
        pass

    pixel_ring.off()
    # except ValueError:
    #     pass

if __name__ == '__main__':
    main()
