import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)

while (1):
    if GPIO.input(15):
        print 'high'
