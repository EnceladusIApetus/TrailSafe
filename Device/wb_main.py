from lib import network, device
import RPi.GPIO as GPIO
import sys, time, json, thread, os

device.set_config('wristband-status', 'normal')
    
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, False)

def check_emergency():
    if device.get_config('wristband-status') == 'normal':
        device.set_config('wristband-status', 'emergency')
        thread.start_new_thread(auto_check_emergency, ())

def auto_check_emergency():
    while(True):
        response = network.check_emergency_response()
        print response
        if response is not None and int(response['emergency-status']) == 93:
            print 'request has been response'
            device.set_config('wristband-status', 'normal')
            GPIO.output(15, True)
            break;
        led_emergency(5, 0.5)

def led_emergency(delay_time, led_interval):
    for x in range(0, delay_time):
        GPIO.output(15, True)
        time.sleep(led_interval/2)
        GPIO.output(15, False)
        time.sleep(led_interval/2)

def emergency(channel):
    network.send_emergency()
    check_emergency()

GPIO.add_event_detect(18, GPIO.FALLING, callback=emergency, bouncetime=300)

while(True):
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
        
