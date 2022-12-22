import time
import RPi.GPIO as GPIO

from subprocess import call

# LED pins
led1 = 7
led2 = 8
led3 = 10
led4 = 11
led5 = 13
led6 = 15
led7 = 16
led8 = 18

led_all = [led1, led2, led3, led4, led5, led6, led7, led8]

# Switch pins
swt1 = 31
swt2 = 29
swt3 = 26
swt4 = 24
swt5 = 23
swt6 = 22
swt7 = 21
swt8 = 19

swt_all = [swt1, swt2, swt3, swt4, swt5, swt6, swt7, swt8]

# Control switches
swt_en = 33
swt_in = 32

swt_ctl = [swt_en, swt_in]

# State
switch_bitmask = 0

def setup_GPIO():
    GPIO.setmode(GPIO.BOARD)

    for pin in led_all:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    for pin in swt_all + swt_ctl:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flash_all():
    for pin in led_all:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)
    for pin in led_all:
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    for pin in led_all:
        GPIO.output(pin, GPIO.LOW)

def read_inputs():
    global switch_bitmask

    switch_bitmask = 0

    for idx, pin in enumerate(swt_all):
        switch_bitmask |= GPIO.input(pin) << idx

def run_enabled():
    return GPIO.input(swt_en) == 0

def input_ready():
    return GPIO.input(swt_in) == 0

def display_binary(num):
    GPIO.output(led1, num & (1 << 0))
    GPIO.output(led2, num & (1 << 1))
    GPIO.output(led3, num & (1 << 2))
    GPIO.output(led4, num & (1 << 3))
    GPIO.output(led5, num & (1 << 4))
    GPIO.output(led6, num & (1 << 5))
    GPIO.output(led7, num & (1 << 6))
    GPIO.output(led8, num & (1 << 7))

def loop():
    
    if run_enabled():
        flash_all()
        time.sleep(1)

        for n in range(256):
            if run_enabled() == False:
                break
            display_binary(n)
            time.sleep(0.4)

        time.sleep(1)

    else:
        read_inputs()
        display_binary(switch_bitmask)

        if input_ready():
            print(switch_bitmask)

            if switch_bitmask == 69:
                print("NICE!")

            if switch_bitmask == 129:
                flash_all()
                time.sleep(0.5)
                call("sudo shutdown -h now", shell=True)
                exit()

        time.sleep(0.1)

def startup():
    flash_all()
    time.sleep(0.5)
    flash_all()
    time.sleep(0.5)
    flash_all()

def main():
    setup_GPIO()
    startup()

    while 1:
        loop()

if __name__  == "__main__":
    main()