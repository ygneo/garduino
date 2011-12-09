import serial
import urllib2
import base64
import json
import time

class ArduinoSerializer(object):
ducksboard_widgets = ["25541", "25542"]
ducksboard_url = 'https://push.ducksboard.com/values/%s/'
ducksboard_api_key = 'c955h3vjqlx1zg1o57ynbb4i6pi252ybw67sloqv48kejqt2f9'

def send_to_widgets(value):
    print value
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


def main(send):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
    while 1:
        try:
            data = ser.readline().strip()
            if data[0]=="#" and data[len(data)-1] == "#":
                value = data.replace("#", "")
        except serial.SerialException:
            pass
        print value
        if send:
            send_to_widgets(value)
    ser.close()


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print ('Usage: %s [send].\nBy default is printing values from serial. If send indicated, it will send data to configured ducksboard widgets' % sys.argv[0])
        sys.exit(0)
    try:
        send = bool(sys.argv[5])
    except Exception:
        send = False

    main(send)
