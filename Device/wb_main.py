from lib import network, device, gpio, wifi_lib
import RPi.GPIO as GPIO
import sys, time, json, thread, os, threading

device.set_config('wristband-status', 'normal')
gpio.set_input_pulldown(gpio.get_pin('switch'))
gpio.on(gpio.get_pin('led-main-system'))
gpio.off(gpio.get_pin('led-alert'))
gpio.off(gpio.get_pin('led-emergency'))
gpio.off(gpio.get_pin('led-signal-coverage'))


def is_coverage():
    signal = -150
    ssids = wifi_lib.get_trailsafe_ssid()
    print ssids
    for ssid in ssids:
	if ssid.signal > signal:
	    signal = ssid.signal
	print 'signal: ' +  str(ssid.signal)

    signal = int(device.get_config('test-signal'))
    if signal > -120:
        gpio.on(gpio.get_pin('led-signal-coverage'))
    else:
        gpio.off(gpio.get_pin('led-signal-coverage'))
    device.set_config('signal-coverage-checking', signal)
    threading.Timer(5.0, is_coverage).start()



def check_emergency():
    if device.get_config('wristband-status') == 'normal':
        device.set_config('wristband-status', 'emergency')
        auto_check_emergency()

def auto_check_emergency():
	 try:
            response = network.check_emergency_response()
            print response
            if response is not None and int(response['emergency-status']) == 93:
                print 'request has been response'
                device.set_config('wristband-status', 'normal')
                gpio.on(gpio.get_pin('led-emergency'))
                return
            gpio.gen_signal(gpio.get_pin('led-emergency'), 5, 0.5)
	    threading.Timer(2, auto_check_emergency).start()
         except:
            print 'an error has occured while checking emergency response'

def emergency(channel):
    network.send_emergency()
    check_emergency()

GPIO.add_event_detect(gpio.get_pin('switch'), GPIO.FALLING, callback=emergency, bouncetime=300)

is_coverage()
print 'test'
#gpio.on(gpio.get_pin('led-signal-coverage'))
while(True):
    
        network.auto_update_status()    

"""while(True):
    try:
        network.auto_update_status()

    except KeyboardInterrupt:
        print 'exit program.'
        GPIO.cleanup()
        sys.exit()
    except:
        report = {}
        report['detail'] = 'an eror has occured in part of server'
        report['sys-info'] = str(sys.exc_info())
        network.send_event(0, json.dumps(report))
        print 'unexpected error: ', sys.exc_info()
        
"""

