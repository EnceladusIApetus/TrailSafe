import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def test(channel):
    print 'interrupt'

GPIO.add_event_detect(18, GPIO.FALLING, callback=test, bouncetime=300)

try:
    while(True):
        'fdfd'
except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
