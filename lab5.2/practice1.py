#Create an infinitely long flashing light. Use an LED connected to GPIO 24.
import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)

while True:
    if(GPIO.input(17) == 0):
        print("Button release")
        GPIO.output(18, 0)
        time.sleep(0.3)
    else: 
        GPIO.output(18, 1)
        print("Button release")
        time.sleep(0.3)
