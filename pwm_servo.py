# This program demonstrates the use of the PCA9685 PWM driver
# This is useful to effectively control multiple servos or motors
# In this example, there is a standard servo on channel 0 and 
# a motor or continuous rotation servo(on channel 2). You can
# also test this code with only one of the two channels in use
# (just don't connect anything to the other channel)

# Libraries
import time
from adafruit_servokit import ServoKit

# Initialize ServoKit for the PWA board.
kit = ServoKit(channels=16)

# Specify the channels you are using on the PWM driver
channel_rotation1 = 0		# Continuous rotation servo
channel_rotation2 = 1
channel_rotation3 = 2
#small normal servos
channel_servo1 = 13 #left
channel_servo2 = 15 #right

# To set the servo range to 180 degrees
# You can adjust the values if needed
kit.servo[channel_servo1].set_pulse_width_range(400,2300)
kit.servo[channel_servo2].set_pulse_width_range(400,2300)
# This is to control a continuous rotation servo
# It does not work for a DC motor
kit.continuous_servo[channel_rotation1].set_pulse_width_range(1200,1800)
kit.continuous_servo[channel_rotation2].set_pulse_width_range(1200,1800)
kit.continuous_servo[channel_rotation3].set_pulse_width_range(1200,1800)

print("Press CTRL+C to end the program.")

print("Starting manual gamepad control. Press Ctrl+C to exit.")
gamepad = InputDevice('/dev/input/event9')  # update device path if needed

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
                    
            noError = True
            while noError:  
                    if (newbutton and codebutton == 305 and valuebutton == 1):
                        
                        channel = channel_rotation1
                        speed = 1
                        kit.continuous_servo[channel].throttle = speed
                        print ('speed: {0} \t channel: {1}'.format(speed,channel))

                    elif (newbutton and codebutton == 306 and valuebutton == 1):
                        channel = channel_rotation2
                        speed = 1
                        kit.continuous_servo[channel].throttle = speed
                        print ('speed: {0} \t channel: {1}'.format(speed,channel))

                        channel = channel_rotation2
                        speed = 1
                        kit.continuous_servo[channel].throttle = speed
                        print ('speed: {0} \t channel: {1}'.format(speed,channel))
                            
                    elif (newbutton and codebutton == 305 and valuebutton == 1):
                        print(" ** Pivot Left **")
                        pivot_left()
                    elif (newbutton and codebutton == 305 and valuebutton == 1):
                        channel = channel_servo1
                        angle = 0
                        kit.servo[channel].angle = angle
                        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                    else:
                        stop()

except KeyboardInterrupt:
        print("Manual control stopped by user.")
        stop()
# Main program 
try:
    noError = True
    while noError:

        channel = channel_servo1
        angle = 0
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 1
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
                
        time.sleep(duration)

        channel = channel_servo1
        angle = 180
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 0.5
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)

        channel = channel_servo1
        angle = 90
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = 0.35
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)

        channel = channel_servo1
        angle = 135
        kit.servo[channel].angle = angle
        print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
        channel = channel_rotation1
        speed = -1.0
        kit.continuous_servo[channel].throttle = speed
        print ('speed: {0} \t channel: {1}'.format(speed,channel))
        
        time.sleep(duration)
        

 
            
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        channel = channel_motor1
        kit.continuous_servo[channel].throttle = 0 
