#Create an infinitely long flashing light. Use an LED connected to GPIO 24.
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM) # GPIO24
 
def blink(pin): 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)
    time.sleep(0.5)
    GPIO.output(pin, 0)
    time.sleep(0.5)


while True:
    blink(24)


GPIO.cleanup()
print("Program finished")

