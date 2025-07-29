import speech_recognition as sr
import cv2
import cv2.aruco as aruco
import numpy as np
import time
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import picamera.array 
from evdev import InputDevice, categorize

# Initialize the camera and grab a reference to the frame
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

# === ArUco Setup ===

# Initialize the recognizer
recognizer = sr.Recognizer()

food=''

# === Marker IDs ===
FOOD_TAGS = {
    "chips": 0,
    "popcorn": 1
}
# Use the default system microphone as the audio source
def listen_for_food():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Say the food you want: 'chips' or 'popcorn'")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        result = recognizer.recognize_google(audio).lower()
        print(f"You said: {result}")
        for food in FOOD_TAGS:
            if food in result:
                return food
    except sr.UnknownValueError:
        print("Sorry, didn't catch that.")
    return None

def drive_to_tag(target_id):
    print(f"Searching for marker ID {target_id}...")
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    
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

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Set PWM parameters
pwm_frequency = 1000 

for pin in [GPIO_Ain1, GPIO_Ain2, GPIO_Apwm, GPIO_Bin1, GPIO_Bin2, GPIO_Bpwm]:
    GPIO.setup(pin, GPIO.OUT)

pwmA = GPIO.PWM(GPIO_Apwm, 1000)
pwmB = GPIO.PWM(GPIO_Bpwm, 1000)
pwmA.start(0)
pwmB.start(0)
# === Motor Control ===
def move_forward(speed=50):
    GPIO.output(GPIO_Ain1, True)
    GPIO.output(GPIO_Ain2, False)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)


try:
    food=listen_for_food()
    if True:#food == 'chips':
        print("moving forward")
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = detector.detectMarkers(gray)

        if ids is not None:
            if target_id in ids:
                idx = list(ids.flatten()).index(target_id)
                c = corners[idx][0]
                cx = int(np.mean(c[:, 0]))
                tag_width = np.linalg.norm(c[0] - c[1])  # proxy for distance

                center_x = 320  # image width / 2

                if cx < center_x - 50:
                    print("↪️ Tag left — Pivoting left")
                    pivot_left()
                elif cx > center_x + 50:
                    print("↩️ Tag right — Pivoting right")
                    pivot_right()
                else:
                    print("⬆️ Aligned — Moving forward")
                    move_forward(45)

                # If close enough (adjust value based on testing)
                if tag_width > 120:
                    print("Close enough! Stopping.")
                    stop()
                    time.sleep(1)
                    break
            else:
                print("Tag not found — Scanning...")
                pivot_left()
        else:
            print("No tags detected — Turning...")
            pivot_left()

        raw_capture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.close()
    stop()
        

except KeyboardInterrupt:
    print("Program interrupted.")
    
