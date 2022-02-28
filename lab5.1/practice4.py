# Create a bi-directional running light with the 4 LEDs of the LED bar. 
# (From left to right and immediately after from right to left)

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

def bi_directional_running_light():
    setup_led(24)
    setup_led(23)
    setup_led(27)
    setup_led(22)
    
    # left-right
    turn_led_on(24)
    time.sleep(0.5)
    turn_led_off(24)
    turn_led_on(23)
    time.sleep(0.5)
    turn_led_off(23)
    turn_led_on(27)
    time.sleep(0.5)
    turn_led_off(27)
    turn_led_on(22)
    time.sleep(0.5)
    turn_led_off(22)
    #right-left
    turn_led_on(27)
    time.sleep(0.5)
    turn_led_off(27)
    turn_led_on(23)
    time.sleep(0.5)
    turn_led_off(23)



while True:
    bi_directional_running_light()
