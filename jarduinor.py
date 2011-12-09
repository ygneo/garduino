#!/usr/bin/python

import sys
import re
import serial
import urllib2
import base64
import json
import time

ducksboard_widgets = ["25541", "25542"]
ducksboard_url = 'https://push.ducksboard.com/values/%s/'
ducksboard_api_key = 'c955h3vjqlx1zg1o57ynbb4i6pi252ybw67sloqv48kejqt2f9'

def send_to_widgets(value):
    for widget in ducksboard_widgets:
        send_to_ducksboard(widget, value)

def send_to_ducksboard(widget, value):
    """
    Given a value to send to ducksboard, builds the JSON encoded
    message and performs the request using the client api key as
    basic auth username (Ducksboard won't check the password).
    """
    msg = {'value': int(value)}
    request = urllib2.Request(ducksboard_url % str(widget))
    auth = base64.encodestring('%s:x' % ducksboard_api_key)
    auth = auth.replace('\n', '')
    request.add_header('Authorization', 'Basic %s' % auth)
    response = urllib2.urlopen(request, json.dumps(msg))


class JarduinoSerializer():
    
    def __init__(self, device, speed=9600, timeout=2):
        self.device = device
        self.speed = speed
        self.timeout = timeout
        self.serial = serial.Serial(self.device, self.speed, timeout=self.timeout)
        self.value_pattern = re.compile("^#[0-9]?[0-9]?[0-9]?[0-9]#$")

    def serialize(self):
        try:
            data = self.serial.readline().strip()
            if self.value_pattern.match(data):
                return data.replace("#", "")
            else: 
                return None
        except serial.SerialException:
            pass
        return value

    def close(self):
        self.serial.close()
       

def main(send):
    serializer = JarduinoSerializer('/dev/ttyACM0')       
    while 1:
        value = serializer.serialize()
        if value:
            print value
            if send:
                send_to_widgets(value)



if __name__ == '__main__':
    if len(sys.argv) < 1:
        print ('Usage: %s [send].\nBy default is printing values from serial. If send indicated, it will send data to configured ducksboard widgets' % sys.argv[0])
        sys.exit(0)
    try:
        send = bool(sys.argv[1] == "send")
    except Exception:
        send = False

    main(send)
