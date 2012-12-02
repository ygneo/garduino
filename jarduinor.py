#!/usr/bin/python
import sys
import re
import serial
import urllib2
import base64
import json
import time


DUCKSBOARD_ENDPOINTS = {"1": {"moisture": ["94419", "94415"],
                              "watering": ["94416"],
                              },
                        "2": {"moisture": ["94420", "94417"],
                              "watering": ["94418"],
                              }
                        }
DUCKSBOARD_ENDPOINT_TEMPLATE = 'https://push.ducksboard.com/values/%s/'
DUCKSBOARD_DEFAULT_API_KEY = 'c955h3vjqlx1zg1o57ynbb4i6pi252ybw67sloqv48kejqt2f9'


class DucksboardPusher(object):
    
    def __init__(self, endpoints=DUCKSBOARD_ENDPOINTS, api_key=DUCKSBOARD_DEFAULT_API_KEY):
        self.endpoints = endpoints
        self.api_key = api_key
    
    def push(self, values):
        print "Pushing to endpoints %s... " % self.endpoints
        endpoint_id, value = values
        self._push_to_endpoints(endpoint_id, value)
        time.sleep(1)
        print "[OK]"

    def _push_to_endpoints(self, endpoint_id, value):
        if value == "w":
            value_type = "watering"
            watering_value = 200
            endpoints = self.endpoints[endpoint_id][value_type]
            self._send_to_endpoints(endpoints, watering_value)
        else:
            value_type = "moisture"
            watering_value = 0
            endpoints = self.endpoints[endpoint_id]["watering"]
            self._send_to_endpoints(endpoints, 0)
            endpoints = self.endpoints[endpoint_id]["moisture"]
            self._send_to_endpoints(endpoints, value)

    def _send_to_endpoints(self, endpoints, value):
        for endpoint in endpoints:
            self._send_to_endpoint(endpoint, value)

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
        

class GarduinoParser(object):
    
    def __init__(self, device, speed=9600, timeout=2):
        self.device = device
        self.speed = speed
        self.timeout = timeout
        self.serial = serial.Serial(self.device, self.speed, timeout=self.timeout)
        self.value_pattern = re.compile("^#([0-9])#([0-9]+|w)#$")

    def parse(self):
        try:
            data = self.serial.readline().strip()
            match = self.value_pattern.match(data)
            if match:
                 return match.groups()
            else: 
                return None
        except serial.SerialException:
            pass
        return value

    def close(self):
        self.serial.close()
       

def main(send):
    parser = GarduinoParser('/dev/ttyACM0')
    pusher = DucksboardPusher()
    while 1:
        values = parser.parse()
        if values:
            print "%s %s" % (time.time(), values)
            if send:
                pusher.push(values)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print ('Usage: %s [send].\nBy default is printing values from serial. If send indicated, it will send data to configured ducksboard widgets' % sys.argv[0])
        sys.exit(0)
    try:
        send = bool(sys.argv[1] == "send")
    except Exception:
        send = False

    main(send)
