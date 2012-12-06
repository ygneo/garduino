#!/usr/bin/python
import sys
import re
import serial
import urllib2
import base64
import json
import time
from libsaas.services import ducksboard

MAX_SENSOR_VALUE = 800
DUCKSBOARD_ENDPOINTS = {"0": {"absolute":
                                  {"moisture": ["94419", "95007"],
                                   "watering": ["95008"],
                                   },
                              "percentage":
                                  {"moisture": ["95379", "95238"],
                                   "watering": ["95380"],
                                   }
                              },
                        "1": {"absolute":
                                  {"moisture": ["94420", "95009"],
                                   "watering": ["95010"],
                                   },
                              "percentage":
                                  {"moisture": ["95381", "95239"],
                                   "watering": ["95382"],
                                   }
                              }
                        }
DUCKSBOARD_API_KEY = 'c955h3vjqlx1zg1o57ynbb4i6pi252ybw67sloqv48kejqt2f9'


class DucksboardPusher(object):
    
    def __init__(self, endpoints=DUCKSBOARD_ENDPOINTS, api_key=DUCKSBOARD_API_KEY):
        self.ducksboard = ducksboard.Ducksboard(api_key)
        self.endpoints = endpoints
                    
    def push(self, values):
        print "Pushing to endpoints %s... " % self.endpoints
        value_id, value = values
        self._push_to_endpoints(value_id, value)
        time.sleep(1)
        print "[OK]"

    def _push_to_endpoints(self, endpoint_id, value):
        if value == "w":
            watering_value = 200
            endpoints = self.endpoints[endpoint_id]["absolute"]["watering"]
            self._send_to_endpoints(endpoints, value=watering_value)
            endpoints = self.endpoints[endpoint_id]["percentage"]["watering"]
            self._send_to_endpoints(endpoints, value=self._percentage(watering_value))
        else:
            endpoints = self.endpoints[endpoint_id]["absolute"]["moisture"]
            self._send_to_endpoints(endpoints, value=value)
            endpoints = self.endpoints[endpoint_id]["percentage"]["moisture"]
            self._send_to_endpoints(endpoints, value=self._percentage(value))
            endpoints = self.endpoints[endpoint_id]["absolute"]["watering"]
            self._send_to_endpoints(endpoints, value=0)
            
    def _percentage(self, value):
        print float(int(value) / float(MAX_SENSOR_VALUE))
        return float(int(value) / float(MAX_SENSOR_VALUE))

    def _send_to_endpoints(self, endpoints, value=None):
        for endpoint in endpoints:
            self._send_to_endpoint(endpoint, value=value)

    def _send_to_endpoint(self, endpoint_id, value=None):
        """
        Given a value to send to ducksboard, builds the JSON encoded
        message and performs the request using the client api key as
        basic auth username (Ducksboard won't check the password).
        """
        self.ducksboard.data_source(endpoint_id).push({"value": value})
 

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

    def close(self):
        self.serial.close()
       

def main(send, serial_device):
    parser = GarduinoParser(serial_device)
    pusher = DucksboardPusher()
    while 1:
        values = parser.parse()
        if values:
            print "%s %s" % (time.time(), values)
            if send:
                pusher.push(values)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print ('Usage: %s [send] -s [serial_device].\nBy default is printing values from serial /dev/ttyACM0.'  
               'If send indicated, it will send data to configured ducksboard widgets' % sys.argv[0])
        sys.exit(0)
    try:
        send = bool(sys.argv[1] == "send")
    except Exception:
        send = False
    try:
        serial_device = sys.argv[2]
    except Exception:
        serial_device = '/dev/ttyACM0'

    main(send, serial_device)
