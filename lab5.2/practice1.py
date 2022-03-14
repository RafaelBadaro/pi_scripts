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
        blink(18)
        print("LED blinks") # button release
        time.sleep(0.3)
    else: 
        GPIO.output(18, 0)
        print("LED not flashing") # button pressed
        time.sleep(0.3)
