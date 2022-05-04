from ctypes import c_bool
import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Value
from datetime import datetime
GPIO.setmode(GPIO.BCM)

# Times
time_begin_night = "20:00:00"
time_almost_midnight = "23:59:59"
time_midnight = "00:00:00"
time_end_night = "06:00:00"

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
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

    GPIO.setup(BUTTON_PUMP, GPIO.IN)
    GPIO.setup(PUMP, GPIO.OUT)

    # setting up
    GPIO.setup(BUTTON_LIGHT, GPIO.IN)
    GPIO.setup(LIGHT, GPIO.OUT)

def get_current_time():
      # TODO - verify time, its getting a strange time  
      time_now = datetime.now()
      time_current = time_now.strftime("%H:%M:%S")
      return time_current

def ultrasound():
    print("Distance Measurement In Progress")

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

            if(distance <= 4.00):
                pump_limit_reached.value = True
                GPIO.output(PUMP, 1) # Turn off 
                print("Pump status: OFF")
            else:
                pump_limit_reached.value = False
            
            print("Distance: ",distance,"cm")
            
    except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        print("Cleaning up!")
        GPIO.cleanup()

def step_motor():

    print("Initializing Stepper Feeder")

    step_sleep = 0.002
    
    step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
    
    direction = False # True for clockwise, False for counter-clockwise
    
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

      # if (button_change_direction is pressed):
      #   direction = True

      # Rotate pallet during certain time
      current_time = get_current_time()
      if((time_begin_night <= current_time <= time_almost_midnight) or 
           (time_midnight <= current_time <= time_end_night)):
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
        

def relay_pump():

    # setting up
    GPIO.output(PUMP, 1) # Turn off the pump

    while True:
        if(pump_limit_reached.value == False):
            if(GPIO.input(BUTTON_PUMP) == 0):    
                GPIO.output(PUMP, 0) # Turn on 
                print("Pump status: ON") 
            elif (GPIO.input(PUMP) == 0):     
                GPIO.output(PUMP, 1) # Turn off 
                print("Pump status: OFF")
            time.sleep(0.3) 
    

def relay_lights():

    isDuringPredefinedTime = False

    GPIO.output(LIGHT, 1) # Turn off the light

    while True:
        # Turn lights on based on time
        current_time = get_current_time()
        if((time_begin_night <= current_time <= time_almost_midnight) or 
           (time_midnight <= current_time <= time_end_night)):
            # If time is between the predefined times, turn on light
            GPIO.output(LIGHT, 0) 
            isDuringPredefinedTime = True
            # TODO - what is the behaviour if the button is pressed during predefined times?
        elif (isDuringPredefinedTime):
            # If time is not in between the predefined times 
            # and the light was turned on during predefined times, turn off light
            GPIO.output(LIGHT, 1)
            isDuringPredefinedTime = False

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
p3 = Process(target=relay_pump)
p3.start()
p4 = Process(target=relay_lights)
p4.start()
p1.join()
p2.join()
p3.join()
p4.join()
