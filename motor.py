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

# === Motor Control Functions ===
def move_forward(speed=50):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    print("Moving forward")

def pivot_left(speed=50):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    print("Pivoting left")

def pivot_right(speed=50):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)
    print("Pivoting right")

def stop():
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    print("Stopped")
print("Press CTRL+C to end the program.")
 
# Main program
try:
        
        noError = True
        while noError:

        move_forward()
        pivot_left()
        pivot_right()
        stop()
   
        # Clean up GPIO if there was an error
        GPIO.cleanup()

        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()
