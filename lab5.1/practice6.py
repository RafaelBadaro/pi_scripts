# Create an SOS signal on output GPIO18. (1 short pulse, 1 long pulse, 1 short pulse) 
# and repeat this continuous.
#  Short pulse = 0.5 s --- Long pulse = 1.5 s ___ ___ ___
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

def sos():
    setup_led(LED1)

    turn_led_on(LED1)
    time.sleep(0.5)
    turn_led_off(LED1)
    time.sleep(0.5)
    turn_led_on(LED1)
    time.sleep(1)
    turn_led_off(LED1)
    time.sleep(1)


while True:
    sos()
