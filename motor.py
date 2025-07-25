# Libraries
import RPi.GPIO as GPIO
import time

 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
GPIO_Ain1 = 11
GPIO_Ain2 = 13
GPIO_Apwm = 15
GPIO_Bin1 = 29
GPIO_Bin2 = 31
GPIO_Bpwm = 33

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

# Set PWM parameters
pwm_frequency = 1000

# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(100)
pwmB.start(100)

gamepad = InputDevice('/dev/input/event4')
print(gamepad)
print("")

# === Motor Control Functions ===
def move_forward(speed=50):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def move_backward(speed = 50):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(speed)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(speed)

def pivot_left(speed=50):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def pivot_right(speed=50):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def stop():
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
print("Press CTRL+C to end the program.")
 
# Main program
try:
        
        noError = True
        while noError:
            # Process the gamepad events
            # This implementation is non-blocking
                         
           move_forward()
           move_backward()
           pivot_left()
           pivot_right()
           stop()

            #gamepad controlled
            newbutton = False
            newstick  = False
            try:
                #for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                eventinfo = categorize(event)
                if event.type == 1:
                    newbutton = True
                    codebutton  = eventinfo.scancode
                    valuebutton = eventinfo.keystate
                elif event.type == 3:
                    newstick = True
                    codestick  = eventinfo.event.code
                    valuestick = eventinfo.event.value
            except:
                pass
        
            if (newstick and codestick == 1 and valuestick < 100):                         
                print (" ** Going Forward **\n")
                move_forward()
            elif (newstick and codestick == 1 and valuestick > 150):
                print (" ** Going Backwards **\n")
                move_backward()
            elif (newstick and codestick == 0 and valuestick < 100):
                print (" ** Pivot Left **\n")
                pivot_left()
            elif (newstick and codestick == 0 and valuestick > 150):
                print (" ** Pivot Right **\n")
                pivot_right()
            else:
                stop()

        # Clean up GPIO if there was an error
        GPIO.cleanup()

        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
