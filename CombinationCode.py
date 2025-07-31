import time
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time

import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

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
        text = recognizer.recognize_google(audio)
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

kit.continuous_servo[channel_rotation1].set_pulse_width_range(500, 2500)
kit.continuous_servo[channel_rotation2].set_pulse_width_range(500, 2500)
kit.continuous_servo[channel_rotation3].set_pulse_width_range(500, 2500)

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

# === Helper Function ===
def stop():
    print("Stopping all motors")
    kit.continuous_servo[channel_rotation1].throttle = 0
    kit.continuous_servo[channel_rotation2].throttle = 0
    kit.continuous_servo[channel_rotation3].throttle = 0

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
  
channel = channel_rotation2
speed = 0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  

channel = channel_rotation3
speed = -0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)

move_forward()
time.sleep(5)

if text == "crackers":
  pivot_left()
  time.sleep(2)

if text == "Popcorn":
  pivot_right()
  time.sleep(2)

channel = channel_servo1
angle = 0
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  

channel = channel_servo2
angle = 90
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
time.sleep(1)

move_backwards()
time.sleep(5)

channel = channel_rotation2
speed = 1
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  

channel = channel_rotation3
speed = -1
kit.continuous_servo[channel].throttle = speed
time.sleep(1)

channel = channel_servo1
angle = 90
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  

channel = channel_servo2
angle = 0
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
time.sleep(1)
