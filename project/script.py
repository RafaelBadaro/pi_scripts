import RPi.GPIO as GPIO
import time
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
            
            print("Waiting For Sensor To Settle")
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
    in1 = 23
    in2 = 22
    in3 = 27
    in4 = 17 

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
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( in1, GPIO.OUT )
    GPIO.setup( in2, GPIO.OUT )
    GPIO.setup( in3, GPIO.OUT )
    GPIO.setup( in4, GPIO.OUT )
    
    # initializing
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    
    
    motor_pins = [in1,in2,in3,in4]
    motor_step_counter = 0
    
    
    def cleanup():
        GPIO.output( in1, GPIO.LOW )
        GPIO.output( in2, GPIO.LOW )
        GPIO.output( in3, GPIO.LOW )
        GPIO.output( in4, GPIO.LOW )
        GPIO.cleanup()
    
    
    # the meat
    try:
        i = 0
        for i in range(step_count):
            for pin in range(0, len(motor_pins)):
                GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
            if direction==True:
                motor_step_counter = (motor_step_counter - 1) % 8
            elif direction==False:
                motor_step_counter = (motor_step_counter + 1) % 8
            else: # defensive programming
                print( "uh oh... direction should *always* be either True or False" )
                cleanup()
                exit( 1 )
            time.sleep( step_sleep )
    
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
    
    cleanup()
    exit( 0 )


#ultrasound()

step_motor()
