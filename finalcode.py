# Libraries
import picamera
import picamera.array
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize, ecodes

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
    
    text = ""
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

speed = 45
a = 8

# === Motor Control Functions ===
def move_forward():
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed+a)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(speed)
    print("Moving forward")

def pivot_left(p):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed + 30*p*0.8)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(speed- 30*p*0.8) 
    print("Pivoting left")

def pivot_right(p):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed - 30 * p *0.8 )               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(speed + 30 * p*0.8)
    print("Pivoting right")

def stop():
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(0)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(0)
    print("Stopped")

def backwards():
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(speed+a)               # duty cycle between 0 and 100
    pwmB.ChangeDutyCycle(speed)

# === Color Detection Thresholds (HSV) ===
lowerColorThreshold = np.array([0, 30, 60])
upperColorThreshold = np.array([20, 150, 255])

# === Camera Setup ===
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = False
camera.hflip = True
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

print("Press CTRL+C to end the program.")


try:
  noError = True
  while (noError):
    time.sleep(0.1)  # Allow camera to warm up
    channel = channel_rotation1
    angle = 45
    kit.servo[channel].angle = angle
      
    for frame in camera.capture_continuous(rawframe, format='bgr', use_video_port=True):
        image = frame.array
        
        
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        ourmask = cv2.inRange(image_hsv, lowerColorThreshold, upperColorThreshold)

        numpixels = cv2.countNonZero(ourmask)
        print("Number of pixels in the color range:", numpixels)

        numx, numy = ourmask.shape
        ourmask_center = ourmask[numx//4:3*numx//4, numy//4:3*numy//4]
        numpixels_center = cv2.countNonZero(ourmask_center)
        print("Number of pixels in center part:", numpixels_center)

        # Bitwise AND for visualization
        image_masked = cv2.bitwise_and(image, image, mask=ourmask)

        # Show frames (optional for debugging)
        cv2.imshow("Frame in BGR", image)
        cv2.imshow("Frame in HSV", image_hsv)
        cv2.imshow("Mask", ourmask)
        cv2.imshow("Masked image", image_masked)
        cv2.waitKey(1)

        # === Navigation Algorithm ===
        WHITE_THRESHOLD = 2000  # Adjust as needed

        # Divide image into thirds      
        left_section = ourmask[:, :numy//3]
        center_section = ourmask[:, numy//3:2*numy//3]
        right_section = ourmask[:, 2*numy//3:]

        white_left = cv2.countNonZero(left_section)
        white_center = cv2.countNonZero(center_section)
        white_right = cv2.countNonZero(right_section)

        print(f"White pixels - L: {white_left}, C: {white_center}, R: {white_right}")

        if white_left > WHITE_THRESHOLD and white_left > white_center and white_left > white_right:
            print("Go left")
            x = ((white_left - white_right) / white_left)
            pivot_left(x)

        elif white_right > WHITE_THRESHOLD and white_right > white_center and white_right > white_left:
            print("Go right")
            x = ((white_right - white_left) / white_right)
            pivot_right(x)

        elif white_center > WHITE_THRESHOLD:
            print("Go straight")
            move_forward()

        elif (white_center < 20):
            print("Stopping")
            stop()
            camera.close()
            
            if text == "crackers":
                print("Going to get crackers")
                channel = channel_rotation1
                angle = 90
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                channel = channel_servo1
                angle = 0
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
            
                channel = channel_servo2
                angle = 90
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
                time.sleep(1)
            
                backwards()
                time.sleep(1)
            
                channel = channel_rotation1
                angle = 135
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                channel = channel_servo1
                angle = 90
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
            
                channel = channel_servo2
                angle = 0
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
                time.sleep(1)
            
                channel = channel_rotation1
                angle = 45
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                backwards()
                time.sleep(3)
                print("I got your snack!")
                stop()
            
            elif text == "Popcorn":
                print("Going to get popcorn")
                channel = channel_rotation1
                angle = 0
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                channel = channel_servo1
                angle = 0
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
            
                channel = channel_servo2
                angle = 90
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
                time.sleep(1)
            
                backwards()
                time.sleep(1)
            
                channel = channel_rotation1
                angle = 135
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                channel = channel_servo1
                angle = 90
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
            
                channel = channel_servo2
                angle = 0
                kit.servo[channel].angle = angle
                print('angle: {0} \t channel: {1}'.format(angle, channel))  
                time.sleep(1)
            
                channel = channel_rotation1
                angle = 45
                kit.servo[channel].angle = angle
                time.sleep(2)
            
                backwards()
                time.sleep(3)
                print("I got your snack!")
                stop()


        # Prepare for next frame
        rawframe.truncate(0)

except KeyboardInterrupt:
    print("Program interrupted by user. Cleaning up...")
    stop()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
    camera.close()
