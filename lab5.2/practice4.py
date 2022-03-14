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

def sos(pin):
    GPIO.output(pin, 1)
    time.sleep(0.5)
    GPIO.output(pin, 0)
    time.sleep(1.5)

    
while True:
    if(GPIO.input(17) == 0):
        # button release
        sos(18)
        print("LED - SOS") 
        time.sleep(0.3)
    else: 
        # button pressed
        GPIO.output(18, 0)
        print("LED no blinking")
        time.sleep(0.3)
