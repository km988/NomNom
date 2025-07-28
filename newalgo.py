import cv2
import cv2.aruco as aruco
import numpy as np
import time
import speech_recognition as sr
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
from evdev import InputDevice, categorize

# === ArUco Setup ===
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, parameters)

# === Marker IDs ===
FOOD_TAGS = {
    "chips": 0,
    "juice": 1
}
HUMAN_ID = 2

# === GPIO Motor Setup ===
GPIO.setmode(GPIO.BOARD)
GPIO_Ain1, GPIO_Ain2, GPIO_Apwm = 11, 13, 15
GPIO_Bin1, GPIO_Bin2, GPIO_Bpwm = 29, 31, 33

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

def move_backward(speed=50):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, False)
    GPIO.output(GPIO_Bin2, True)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def pivot_left(speed=40):
    GPIO.output(GPIO_Ain1, False)
    GPIO.output(GPIO_Ain2, True)
    GPIO.output(GPIO_Bin1, True)
    GPIO.output(GPIO_Bin2, False)
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def pivot_right(speed=40):
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

# === Voice Input ===
def listen_for_food():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎤 Say the food you want: 'chips' or 'juice'")
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

# === Vision-Based Drive to Tag ===
def drive_to_tag(target_id):
    print(f"Searching for marker ID {target_id}...")
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

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
                    print("📦 Close enough! Stopping.")
                    stop()
                    time.sleep(1)
                    break
            else:
                print("🔁 Tag not found — Scanning...")
                pivot_left()
        else:
            print("🔍 No tags detected — Turning...")
            pivot_left()

        raw_capture.truncate(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.close()
    stop()

# === Your gamepad control section integrated ===
def gamepad_control():
    print("🎮 Starting manual gamepad control. Press Ctrl+C to exit.")
    gamepad = InputDevice('/dev/input/event4')  # update device path if needed

    try:
        while True:
            newbutton = False
            newstick = False
            try:
                event = gamepad.read_one()
                if event is None:
                    continue
                eventinfo = categorize(event)
                if event.type == 1:  # Button event
                    newbutton = True
                    codebutton = eventinfo.scancode
                    valuebutton = eventinfo.keystate
                elif event.type == 3:  # Analog stick event
                    newstick = True
                    codestick = eventinfo.event.code
                    valuestick = eventinfo.event.value
            except:
                continue

            if newstick and codestick == 1 and valuestick < 100:
                print(" ** Going Forward **")
                move_forward()
            elif newstick and codestick == 1 and valuestick > 150:
                print(" ** Going Backwards **")
                move_backward()
            elif newstick and codestick == 0 and valuestick < 100:
                print(" ** Pivot Left **")
                pivot_left()
            elif newstick and codestick == 0 and valuestick > 150:
                print(" ** Pivot Right **")
                pivot_right()
            else:
                stop()

    except KeyboardInterrupt:
        print("Manual control stopped by user.")
        stop()

# === Main program with mode choice ===
try:
    mode = input("Choose mode ('auto' or 'manual'): ").strip().lower()
    if mode == 'manual':
        gamepad_control()
    elif mode == 'auto':
        while True:
            food_choice = None
            while food_choice is None:
                food_choice = listen_for_food()

            food_id = FOOD_TAGS[food_choice]

            print(f"🚗 Going to get '{food_choice}' (marker ID {food_id})")
            drive_to_tag(food_id)

            print("🤖 Ready to grab! Use robot arm now.")
            time.sleep(5)  # Time to grab manually

            print("🔙 Returning to human (ID 2)...")
            drive_to_tag(HUMAN_ID)

            print("✅ Task complete. Waiting for next command...\n")

    else:
        print("Invalid mode selected. Exiting.")

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    stop()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()
