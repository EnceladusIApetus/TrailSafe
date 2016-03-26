import RPi.GPIO as GPIO
import device, time

def get_pin(pin_name):
    gpio_pin = device.get_config('gpio-pin')
    return int(gpio_pin[pin_name])

def set_input(pin):
    GPIO.setup(pin, GPIO.IN)

def set_output(pin):
    GPIO.setup(pin, GPIO.OUT)

def init():
    GPIO.setmode(GPIO.BCM)

def set_input_pulldown(pin):
    init()
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def set_input_pullup(pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def on(pin):
    init()
    set_output(pin)
    GPIO.output(pin, True)

def off(pin):
    init()
    set_output(pin)
    GPIO.output(pin, False)

def gen_signal(pin, delay_time, period):
    for x in range(0, delay_time):
        on(pin)
        time.sleep(period/2)
        off(pin)
        time.sleep(period/2)

def clear():
    GPIO.cleanup()

