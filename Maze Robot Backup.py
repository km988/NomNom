# This program illustrates how to capture frames in a video stream and
# and how to do extract pixels of a specific color
# It uses openCV
import picamera
import picamera.array                                   # This needs to be imported explicitly
import cv2
import time
import numpy as np                                      
# Libraries
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
pwmA.start(100)
pwmB.start(100)

#def wheelControl(vforward,vturn):
#    l = 1
#    vleft = l*vturn*0.5 + vforward
#    vright = vforward - l*vturn*0.5
    
#    return vleft, vright



# Define the range colors to filter; these numbers represent HSV
lowerColorThresholdO = np.array([0, 0, 20])
upperColorThresholdO = np.array([10, 255, 255])
lowerColorThresholdP = np.array([130, 0, 0])
upperColorThresholdP = np.array([140, 255, 255])


# Initialize the camera and grab a reference to the frame
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = False                            # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))


print("Press CTRL+C to end the program.")

try:

        # Allow the camera to warm up
        time.sleep(0.1)
        
        # Continuously capture frames from the camera
        # Note that the format is BGR instead of RGB because we want to use openCV later on and it only supports BGR
        for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
                        
            # Create a numpy array representing the image
            image = frame.array     

            #-----------------------------------------------------
            # We will use numpy and OpenCV for image manipulations
            #-----------------------------------------------------

            # Convert for BGR to HSV color space, using openCV
            # The reason is that it is easier to extract colors in the HSV space
            # Note: the fact that we are using openCV is why the format for the camera.capture was chosen to be BGR
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Threshold the HSV image to get only colors in a range
            # The colors in range are set to white (255), while the colors not in range are set to black (0)
            ourmask = cv2.inRange(image_hsv, lowerColorThresholdO, upperColorThresholdO)
            purplemask = cv2.inRange(image_hsv, lowerColorThresholdP, upperColorThresholdP)

            
            
            # Get the size of the array (the mask is of type 'numpy')
            # This should be 640 x 480 as defined earlier
            numx, numy = ourmask.shape

            # Select a part of the image and count the number of white pixels
            #ourmask_O = ourmask[ 0 : numx , 0 : numy ]
            numpixels_O = cv2.countNonZero(ourmask)
            #ourmask_P = purplemask[ 0 : numx , 0 : numy ]
            numpixels_P = cv2.countNonZero(purplemask)
            
            if text=="chips":
                #numpixels = cv2.countNonZero(purplemask)
                if numpixels_P > 6000:
                    #####CHANGE TO SERVO MOVEMENT
                
                else:
                    M = cv2.moments(purplemask)
                        
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    #if sticky note on left of screen
                    if (cX < 310):
                        #leftWheel, rightWheel = wheelControl(50, (numx/2 - cX)*0.2)
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(40 - (320 - cX)*0.1)                
                        pwmB.ChangeDutyCycle(40)
                        print("turn left");
                    elif (330 < cX):
                        #leftWheel, rightWheel = wheelControl(50, (cX - numx/2)*0.2)
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(40)                
                        pwmB.ChangeDutyCycle(40 - (cX - 320)*0.1)
                        print("turn right")
                    else:
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(20)                
                        pwmB.ChangeDutyCycle(20)
               
                    # Bitwise AND of the mask and the original image
                    image_masked = cv2.bitwise_and(image, image, mask = purplemask)
                    cv2.imshow("Mask", purplemask)
                
            elif text=="juice":
                # Count the number of white pixels in the mask
                #numpixels = cv2.countNonZero(ourmask)
                if numpixels_O > 6000:
                    ####CHANGE TO SERVO CODE
                else:
                    M = cv2.moments(ourmask)
                        
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    #if sticky note on left of screen
                    if (cX < 310):
                        #leftWheel, rightWheel = wheelControl(50, (numx/2 - cX)*0.2)
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(40 - (numx/2 - cX)*0.1)                
                        pwmB.ChangeDutyCycle(40)
                        print("turn left");
                    elif (330 < cX):
                        #leftWheel, rightWheel = wheelControl(50, (cX - numx/2)*0.2)
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(40 - (numx/2 - cX)*0.1)                
                        pwmB.ChangeDutyCycle(40)
                        print("turn right")
                    else:
                        GPIO.output(GPIO_Ain1, True)
                        GPIO.output(GPIO_Ain2, False)
                        GPIO.output(GPIO_Bin1, False)
                        GPIO.output(GPIO_Bin2, True)
                        pwmA.ChangeDutyCycle(40)                
                        pwmB.ChangeDutyCycle(40)
               
                    # Bitwise AND of the mask and the original image
                    image_masked = cv2.bitwise_and(image, image, mask = ourmask)
                    cv2.imshow("Mask", ourmask)


            # Show the frames
            # The waitKey command is needed to force openCV to show the image
            #cv2.imshow("Frame in BGR", image)
            #cv2.imshow("Frame in HSV", image_hsv)
            #cv2.imshow("Masked image", image_masked)  
            cv2.waitKey(1)

            # Clear the stream in preparation for the next frame
            rawframe.truncate(0)
        
  
# Quit the program when the user presses CTRL + C
except:
        # Clean up the resources
        GPIO.output(GPIO_Ain1, False)
        GPIO.output(GPIO_Ain2, False)
        GPIO.output(GPIO_Bin1, False)
        GPIO.output(GPIO_Bin2, False)
        cv2.destroyAllWindows()
        camera.close()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()

