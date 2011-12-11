#!/usr/bin/python

import sys
import re
import serial
import urllib2
import base64
import json
import time

DUCKSBOARD_ENDPOINT_IDS = ["25541", "25542"]
DUCKSBOARD_ENDPOINT_TEMPLATE = 'https://push.ducksboard.com/values/%s/'
DUCKSBOARD_DEFAULT_API_KEY = 'c955h3vjqlx1zg1o57ynbb4i6pi252ybw67sloqv48kejqt2f9'

class DucksboardEmitter(object):

    def __init__(self, endpoints_ids, api_key=DUCKSBOARD_DEFAULT_API_KEY):
        self.endpoints_ids = endpoints_ids
        self.api_key = api_key
    
    def send(self, value):
        print "Sending to endpoints %s... " % self.endpoints_ids,
        for endpoint in self.endpoints_ids:
            self._send_to_endpoint(endpoint, value)
        print "[OK]"

    def _send_to_endpoint(self, endpoint, value):
        """
        Given a value to send to ducksboard, builds the JSON encoded
        message and performs the request using the client api key as
        basic auth username (Ducksboard won't check the password).
        """
        msg = {'value': int(value)}
        request = urllib2.Request(DUCKSBOARD_ENDPOINT_TEMPLATE % str(endpoint))
        auth = base64.encodestring('%s:x' % self.api_key)
        auth = auth.replace('\n', '')
        request.add_header('Authorization', 'Basic %s' % auth)
        response = urllib2.urlopen(request, json.dumps(msg))
        

class JarduinoSerializer(object):
    
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
    emitter = DucksboardEmitter(DUCKSBOARD_ENDPOINT_IDS)
    while 1:
        value = serializer.serialize()
        if value:
            print "%s,%s" % (time.time(), value)
            if send:
                emitter.send(value)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print ('Usage: %s [send].\nBy default is printing values from serial. If send indicated, it will send data to configured ducksboard widgets' % sys.argv[0])
        sys.exit(0)
    try:
        send = bool(sys.argv[1] == "send")
    except Exception:
        send = False

    main(send)
