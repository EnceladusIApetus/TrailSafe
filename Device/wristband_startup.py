from lib import hotspot, device, connectNode, gpio, wifi_lib
import os, threading, time
import RPi.GPIO as GPIO

gpio.init()
gpio.clear()
gpio.set_output(gpio.get_pin('led-main-system'))
gpio.set_output(gpio.get_pin('led-signal-coverage'))
gpio.set_output(gpio.get_pin('led-alert'))
gpio.set_output(gpio.get_pin('led-wifi-connection'))
gpio.set_output(gpio.get_pin('led-emergency'))

def loop_led():
    if device.get_config('server-connection') == 'not connect':
        gpio.gen_signal(gpio.get_pin('led-wifi-connection'), 5, 0.5)
	threading.Timer(2, loop_led).start()


def is_coverage():
    try:
	signal = -150
    	ssids = wifi_lib.get_trailsafe_ssid()
    	print ssids
    	for ssid in ssids:
	    if ssid.signal > signal:
	    	signal = ssid.signal
	    print 'signal: ' +  str(ssid.signal)
    
    	#signal = int(device.get_config('signal-coverage-checking'))
    	if signal > -120:
	    gpio.on(gpio.get_pin('led-signal-coverage'))
	    print 'high signal'
    	else:
	    gpio.off(gpio.get_pin('led-signal-coverage'))
	    print 'low signal'
    	device.set_config('signal-coverage-checking', signal)
    	threading.Timer(5.0, is_coverage).start()
    except:
    	threading.Timer(5.0, is_coverage).start()	    

is_coverage()

while(True):
    
        device.set_config('server-connection', 'not connect')
        loop_led()
        while connectNode.connect_node() == False:
            print 'error: connect connect to server connected ssid'
        gpio.clear()
        #gpio.on(gpio.get_pin('led-wifi-connection'))
        print 'hihi'
        os.popen('python /home/pi/TrailSafe/Device/wb_main.py')
        gpio.off(gpio.get_pin('led-main-system'))
    
        print 'error has occured in main session'
    
