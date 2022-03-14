import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

def blink(pin): 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    time.sleep(0.1)
    GPIO.output(pin, 0)

while True:
    if(GPIO.input(17) == 0):
        GPIO.output(18, 0)
        print("LED not flashing") # button pressed
        time.sleep(0.3)
    else: 
        blink(18)
        print("LED blinks") # button release
        time.sleep(0.3)


# THIS CODE WAS USED ON A RELAY BOARD. THE RELAY BOARD MAKES A 'TICK' SOUND WHEN THE LIGHT IS BLINKING
# THE LIGHT ON THE RELAY STARTS AS 'ON'