# Make a flashing light of the 4 LEDs (together on, together off)
# with a waiting time of 0.1 seconds between on and off. Choose which GPIO pins you use for this.

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO24
 
# LED Mappings
# GPIO 24 - IN1 - A (First LED)
# GPIO 23 - IN2 - B
# GPIO 27 - IN3 - C
# GPIO 22 - IN4 - D

def setup_led(pin):
    GPIO.setup(pin, GPIO.OUT)

def turn_led_on(pin):
    GPIO.output(pin, 1)

def turn_led_off(pin):
    GPIO.output(pin, 0)

def blink_together():
    setup_led(24)
    setup_led(23)
    setup_led(27)
    setup_led(22)

    turn_led_on(24)
    turn_led_on(23)
    turn_led_on(27)
    turn_led_on(22)

    time.sleep(0.1)

    turn_led_off(24)
    turn_led_off(23)
    turn_led_off(27)
    turn_led_off(22)
    
    time.sleep(0.1)

while True:
    blink_together()
