import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO24



def blink(pin, aantalBlinks, periode, dutyCycle):
    GPIO.setup(pin, GPIO.OUT)
    tijdhoog = periode * dutyCycle/100
    tidjlaag = periode - tijdhoog

    for teller in range(0, aantalBlinks): # makes it blink 20 times
            GPIO.output(pin, GPIO.HIGH) # turns on the led
            time.sleep(tijdhoog) 
            GPIO.output(pin, GPIO.LOW) # turns off the led
            time.sleep(tidjlaag)
            

blink(24, 20, 0.5, 75)

GPIO.cleanup()
print("Program finished")