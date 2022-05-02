import RPi.GPIO as GPIO
import time
from multiprocessing import Process
GPIO.setmode(GPIO.BCM)

def ultrasound():
    # Set GPIO's
    TRIG = 5
    ECHO = 6

    print("Distance Measurement In Progress")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    try:
        while True:
            
            #print("Waiting For Sensor To Settle")
            time.sleep(0.5)

            GPIO.output(TRIG, GPIO.HIGH) # Setting TRIG port to high
            time.sleep(0.00001) # Start the module with a trigger pulse of 10μs on the trigger input
            GPIO.output(TRIG, GPIO.LOW) # Setting TRIG port to low
            

            # The pulsewidth of the echo pulse is a measure for the distance
            # Set ECHO to low
            while GPIO.input(ECHO) == GPIO.LOW:
                pulse_start = time.time()
            
            # Set ECHO to high
            while GPIO.input(ECHO) == GPIO.HIGH:
                pulse_end = time.time()
            
            # Get the duration of the pulse
            pulse_duration = pulse_end - pulse_start
            
            # Get the distance in cm
            distance = pulse_duration * 17000
            
            # Round it for better visualization
            distance = round(distance, 2)
            
            print("Distance: ",distance,"cm")
            
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        print("Cleaning up!")
        GPIO.cleanup()


def step_motor():

    print("Initializing Stepper Feeder")

    in1 = 23
    in2 = 22
    in3 = 27
    in4 = 17 
    button1 = 24

    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    step_sleep = 0.002
    
    step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
    
    direction = False # True for clockwise, False for counter-clockwise
    
    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]
    
    # setting up
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(button1, GPIO.IN)
    
    # initializing
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
     
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0
    
    
    def shutdown_leds():
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

    def cleanup():
        shutdown_leds()
        GPIO.cleanup()
    
    while(True):

      while(GPIO.input(button1) == 1):
            # Rotate the motor
        try:
                i = 0
                for i in range(step_count):
                    if(GPIO.input(button1) == 0): 
                        # If the button is released it stops
                        shutdown_leds()
                        break 
                    for pin in range(0, len(motor_pins)):
                        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
                    if direction==True:
                        motor_step_counter = (motor_step_counter - 1) % 8
                    elif direction==False:
                        motor_step_counter = (motor_step_counter + 1) % 8
                    else: # defensive programming
                        print( "uh oh... direction should *always* be either True or False" )
                        cleanup()
                        exit(1)
                    time.sleep(step_sleep)
            
        except KeyboardInterrupt:
            cleanup()
            exit(1)
        

def relay_pump():
    button_pump = 26
    pump = 16 # pump

    # setting up
    GPIO.setup(button_pump, GPIO.IN)
    GPIO.setup(pump, GPIO.OUT)
    GPIO.output(pump, 1) # Turn off the pump

    while True:
        if(GPIO.input(button_pump) == 0):    
            GPIO.output(pump, 0) # Turn on 
            print("Pump status: ON") 
        elif (GPIO.input(pump) == 0):     
            GPIO.output(pump, 1) # Turn off 
            print("Pump status: OFF")

        time.sleep(0.3) 
    


def relay_lights():
    button_light = 25
    light = 8 # light

     # setting up
    GPIO.setup(button_light, GPIO.IN)
    GPIO.setup(light, GPIO.OUT)
    GPIO.output(light, 1) # Turn off the light

    while True:
        if(GPIO.input(button_light) == 0):            
              if(GPIO.input(light) == 1):  # If light is off
                  GPIO.output(light, 0) # Turn on 
                  print("Light status: ON") 
              elif(GPIO.input(light) == 0): # If light is on
                  GPIO.output(light, 1) # Turn off 
                  print("Light status: OFF")
              time.sleep(0.3) 


# Execute the methods
p1 = Process(target=ultrasound)
p1.start()
p2 = Process(target=step_motor)
p2.start()
p3 = Process(target=relay_pump)
p3.start()
p4 = Process(target=relay_lights)
p4.start()
p1.join()
p2.join()
p3.join()
p4.join()
