# First let LED1 and LED3 go on and off together, then LED2 and LED4 with an interval of 1 second

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO24
 
# LED Mappings
# GPIO 24 - IN1 - A (First LED)
# GPIO 23 - IN2 - B
# GPIO 27 - IN3 - C
# GPIO 22 - IN4 - D

LED1 = 24
LED2 = 23
LED3 = 27
LED4 = 22

def setup_led(pin):
    GPIO.setup(pin, GPIO.OUT)

def turn_led_on(pin):
    GPIO.output(pin, 1)

def turn_led_off(pin):
    GPIO.output(pin, 0)

def blink_1and3_then_2and4():
    setup_led(LED1)
    setup_led(LED2)
    setup_led(LED3)
    setup_led(LED4)

    turn_led_on(LED1)
    turn_led_on(LED3)
    time.sleep(0.5)
    turn_led_off(LED1)
    turn_led_off(LED3)

    time.sleep(1)

    turn_led_on(LED2)
    turn_led_on(LED4)
    time.sleep(0.5)
    turn_led_off(LED2)
    turn_led_off(LED4)
    
    time.sleep(1)

while True:
    blink_1and3_then_2and4()
