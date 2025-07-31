import time
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time

import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()
text = ''

# Use the default system microphone as the audio source
with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=1)  # optional, to improve accuracy
    print("Listening... Speak now!")

    # Listen to the first phrase and store it in audio
    audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
      
# === Configuration ===
kit = ServoKit(channels=16)

# Channel Definitions
channel_rotation1 = 0  # Continuous rotation servo
channel_rotation2 = 1
channel_rotation3 = 2

channel_servo1 = 12  # Standard servo (left arm)
channel_servo2 = 15  # Standard servo (right arm)

# Set pulse width range
kit.servo[channel_servo1].set_pulse_width_range(500, 2500)
kit.servo[channel_servo2].set_pulse_width_range(500, 2500)

kit.servo[channel_rotation1].set_pulse_width_range(500, 2500)
kit.continuous_servo[channel_rotation2].set_pulse_width_range(500, 2500)
kit.continuous_servo[channel_rotation3].set_pulse_width_range(500, 2500)

GPIO.setmode(GPIO.BCM)

motor_speed = 50
 
# set GPIO Pins
GPIO_Ain1 = 17
GPIO_Ain2 = 27
GPIO_Apwm = 22
GPIO_Bin1 = 5
GPIO_Bin2 = 6
GPIO_Bpwm = 13

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Set PWM parameters
pwm_frequency = 1000

# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(0)
pwmB.start(0)

# === Helper Function ===

def move_forward(motor_speed):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(motor_speed)
    pwmB.ChangeDutyCycle(motor_speed)

def move_backward(motor_speed):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(motor_speed)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(motor_speed)
  
def pivot_left(motor_speed):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(motor_speed)
    pwmB.ChangeDutyCycle(motor_speed)

def pivot_right(speed):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(motor_speed)
    pwmB.ChangeDutyCycle(motor_speed)
  
channel = channel_rotation1
angle = 45
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
'''
channel = channel_rotation2
speed = 0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  

channel = channel_rotation3
speed = -0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
'''
move_backward(50)
print("Moving forward")
time.sleep(2)

if text == "crackers":
  pivot_left(50)
  print("Pivoting left")
  time.sleep(0.5)

elif text == "popcorn":
  pivot_right(50)
  print("Pivoting right")
  time.sleep(0.5)
 

channel = channel_servo1
angle = 0
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  

channel = channel_servo2
angle = 90
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
time.sleep(1)

if text == "crackers":
  pivot_right(50)
  time.sleep(0.5)

elif text == "popcorn":
  pivot_left(50)
  time.sleep(0.5)
  
channel = channel_rotation1
angle = 135
kit.servo[channel].angle = angle
time.sleep(1)
'''
channel = channel_rotation2
speed = 1
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  

channel = channel_rotation3
speed = -1
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
'''
channel = channel_servo1
angle = 90
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  

channel = channel_servo2
angle = 0
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
time.sleep(1)

move_forward(50)
time.sleep(2)

GPIO.cleanup()
