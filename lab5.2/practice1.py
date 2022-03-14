#Create an infinitely long flashing light. Use an LED connected to GPIO 24.
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
        print("Button release")
        time.sleep(0.3)
    else: 
        GPIO.output(18, 0)
        print("Button pressed")
        time.sleep(0.3)
 



GPIO.cleanup()
print("Program finished")

