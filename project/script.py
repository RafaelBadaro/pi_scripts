from ctypes import c_bool
import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Value
from datetime import datetime
GPIO.setmode(GPIO.BCM)

# Times
time_light_on_begin = "06:00:00"
time_light_on_end = "20:00:00"
time_rotate_pallet = "17:00:00"

# GPIO's

# ultrasound
TRIG = 5
ECHO = 6
pump_limit_reached = Value(c_bool, False)

# step motor
IN1 = 23
IN2 = 22
IN3 = 27
IN4 = 17 
BUTTON_ROTATE_STEPMOTOR = 24
BUTTON_CHANGE_DIRECTION_STEPMOTOR = 15

# pump 
BUTTON_PUMP = 26
PUMP = 16 # pump

# light 
BUTTON_LIGHT = 25
LIGHT = 8 # light

def setup_gpios():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(BUTTON_ROTATE_STEPMOTOR, GPIO.IN)
    GPIO.setup(BUTTON_CHANGE_DIRECTION_STEPMOTOR, GPIO.IN)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

    GPIO.setup(BUTTON_PUMP, GPIO.IN)
    GPIO.setup(PUMP, GPIO.OUT)

    GPIO.setup(BUTTON_LIGHT, GPIO.IN)
    GPIO.setup(LIGHT, GPIO.OUT)


def get_current_time():
      time_now = datetime.now()
      time_current = time_now.strftime("%H:%M:%S")
      return time_current


def ultrasound():
    print("Distance Measurement In Progress")

    try:
        while True:
            
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

            if(distance > 10.00):
                GPIO.output(PUMP, 0) # Turn on 
                print("Pump status: ON")
            elif(distance <= 4.00):
                GPIO.output(PUMP, 1) # Turn off 
                print("Pump status: OFF")
            else:
                if(GPIO.input(BUTTON_PUMP) == 0):    
                    GPIO.output(PUMP, 0) # Turn on 
                    print("Pump status: ON") 
                elif (GPIO.input(BUTTON_PUMP) == 1):    
                    GPIO.output(PUMP, 1) # Turn off 
                    print("Pump status: OFF")
                time.sleep(0.3) 

            
            print("Distance: ",distance,"cm")
            
    except KeyboardInterrupt:
        print("Cleaning up!")
        GPIO.cleanup()


def step_motor():

    print("Initializing Stepper Feeder")

    step_sleep = 0.002
    
    step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
    
    direction = False # True for counter-clockwise , False for counter-clockwise clockwise
    
    step_sequence = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]
     
    motor_pins = [IN1,IN2,IN3,IN4]
    motor_step_counter = 0   
    
    def shutdown_leds():
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

    def cleanup():
        shutdown_leds()
        GPIO.cleanup()
    
    while(True):

      if(GPIO.input(BUTTON_CHANGE_DIRECTION_STEPMOTOR) == 0):
          if(direction == False):
              direction = True
              print("Direction changed to: counter-clockwise")
          else:
              direction = False
              print("Direction changed to: clockwise")
          time.sleep(0.5)

      # Rotate pallet during certain time
      current_time = get_current_time()
      if(current_time == time_rotate_pallet):
            try:
                i = 0
                for i in range(1024): # 4096 steps is 360°, so 1024 steps is 90°
                    for pin in range(0, len(motor_pins)):
                        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
                    if direction==True:
                        motor_step_counter = (motor_step_counter - 1) % 8
                    elif direction==False:
                        motor_step_counter = (motor_step_counter + 1) % 8
                    time.sleep(step_sleep)
            
            except KeyboardInterrupt:
                cleanup()
                exit(1)

      # Rotate forward one pellet
      if(GPIO.input(BUTTON_ROTATE_STEPMOTOR) == 1):
            try:
                i = 0
                for i in range(1024): # 4096 steps is 360°, so 1024 steps is 90°
                    for pin in range(0, len(motor_pins)):
                        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
                    if direction==True:
                        motor_step_counter = (motor_step_counter - 1) % 8
                    elif direction==False:
                        motor_step_counter = (motor_step_counter + 1) % 8
                    time.sleep(step_sleep)
            
            except KeyboardInterrupt:
                cleanup()
                exit(1)

      # Rotate while button pressed
      while(GPIO.input(BUTTON_ROTATE_STEPMOTOR) == 1):
        try:
                i = 0
                for i in range(step_count):
                    if(GPIO.input(BUTTON_ROTATE_STEPMOTOR) == 0): 
                        # If the button is released it stops
                        shutdown_leds()
                        break 
                    for pin in range(0, len(motor_pins)):
                        GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
                    if direction==True:
                        motor_step_counter = (motor_step_counter - 1) % 8
                    elif direction==False:
                        motor_step_counter = (motor_step_counter + 1) % 8
                    time.sleep(step_sleep)
            
        except KeyboardInterrupt:
            cleanup()
            exit(1)
            
def relay_lights():

    lightOnDuringPredefinedTime = False
    buttonWasPressed = False

    GPIO.output(LIGHT, 1) # Turn off the light

    while True:
        # Turn lights on based on time
        current_time = get_current_time()
        if(time_light_on_begin <= current_time <= time_light_on_end):
            # If time is between the predefined times, turn on light
            # If the button was not pressed we turn on the light
            if(buttonWasPressed == False):
                GPIO.output(LIGHT, 0) 
                lightOnDuringPredefinedTime = True
            else:
                GPIO.output(LIGHT, 1)
                lightOnDuringPredefinedTime = False
            
            # When button is pressed
            if(GPIO.input(BUTTON_LIGHT) == 0):
                if(buttonWasPressed == False):
                    buttonWasPressed = True # Light was turned off by the user
                else:
                    buttonWasPressed = False # Light was turned on by the user
                time.sleep(0.2)

        elif (lightOnDuringPredefinedTime):
            # If time is not in between the predefined times 
            # and the light was turned on during predefined times, turn off light
            GPIO.output(LIGHT, 1)
            lightOnDuringPredefinedTime = False
        else:
            # Button to turn light on and off
            if(GPIO.input(BUTTON_LIGHT) == 0):            
                if(GPIO.input(LIGHT) == 1):  # If light is off
                    GPIO.output(LIGHT, 0) # Turn on 
                    print("Light status: ON") 
                elif(GPIO.input(LIGHT) == 0): # If light is on
                    GPIO.output(LIGHT, 1) # Turn off 
                    print("Light status: OFF")
                time.sleep(0.3)

               

# Execute the methods
setup_gpios()
p1 = Process(target=ultrasound)
p1.start()
p2 = Process(target=step_motor)
p2.start()
p3 = Process(target=relay_lights)
p3.start()
p1.join()
p2.join()
p3.join()

