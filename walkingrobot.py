# This program demonstrates the use of the PCA9685 PWM driver
# This is useful to effectively control multiple servos
# In this example, there is a standard servo on channel 0.

# Libraries
import time
from evdev import InputDevice, categorize

# This library uses BCM numbering!!!!
from adafruit_servokit import ServoKit

gamepad = InputDevice('/dev/input/event4')
print(gamepad)
print("")

# Initialize ServoKit for the PWA board.
kit = ServoKit(channels=16)

# Specify the channels you are using on the PWM driver
channel_servo1 = 7
channel_servo2 = 8
channel_servo3 = 9


# To set the servo range to 180 degrees for the standard servos
# You can adjust the values if needed
kit.servo[channel_servo1].set_pulse_width_range(400,2300)
kit.servo[channel_servo2].set_pulse_width_range(400,2300)
kit.servo[channel_servo3].set_pulse_width_range(400,2300)

    

print("Press CTRL+C to end the program.")


# Keep track of the state
FSM1State = 0
FSM1NextState = 0

# Keep track of the timing
FSM1LastTime = 0
duration = 2

# Process the gamepad events
# This implementation is non-blocking
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


# Main program 
try:
        
    noError = True
    while noError:

        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState

        if (newbutton and codebutton == 308 and valuebutton == 1):                         
            print("Autonomous")
            channel7 = channel_servo1
            channel8 = channel_servo2
            channel9 = channel_servo3
            #move arms back, push body forward
            m3 = 90
            kit.servo[channel9].angle = m3
            print ('angle: {0} \t channel: {1}'.format(m3,channel9))

            m1 = 100
            kit.servo[channel7].angle = m1
            print ('angle: {0} \t channel: {1}'.format(m1,channel7))
                    
            m2 = 180
            kit.servo[channel8].angle = m2
            print ('angle: {0} \t channel: {1}'.format(m2,channel8))
                    
            time.sleep(2)
            #move arms forward, body lifted
            m3 = 180
            kit.servo[channel9].angle = m3
            print ('angle: {0} \t channel: {1}'.format(m3,channel9))
                        
            m1 = 180
            kit.servo[channel7].angle = m1
            print ('angle: {0} \t channel: {1}'.format(m1,channel7))
                        
            m2 = 100
            kit.servo[channel8].angle = m2
            print ('angle: {0} \t channel: {1}'.format(m2,channel8))


        elif (newbutton and codebutton == 309 and valuebutton == 1):                         
            print("Manual")
            if (newbutton and codebutton == 305 and valuebutton == 1): 
                channel7 = channel_servo1
                channel8 = channel_servo2
                channel9 = channel_servo3
                #move bakcwards
                m3 = 90
                kit.servo[channel9].angle = m3
                print ('angle: {0} \t channel: {1}'.format(m3,channel9))

                m1 = 100
                kit.servo[channel7].angle = m1
                print ('angle: {0} \t channel: {1}'.format(m1,channel7))
                    
                m2 = 180
                kit.servo[channel8].angle = m2
                print ('angle: {0} \t channel: {1}'.format(m2,channel8))
                    
            elif (newbutton and codebutton == 306 and valuebutton == 1): 
                channel7 = channel_servo1
                channel8 = channel_servo2
                channel9 = channel_servo3
                #move forward, body lifted
                m3 = 180
                kit.servo[channel9].angle = m3
                print ('angle: {0} \t channel: {1}'.format(m3,channel9))
                        
                m1 = 180
                kit.servo[channel7].angle = m1
                print ('angle: {0} \t channel: {1}'.format(m1,channel7))
                        
                m2 = 100
                kit.servo[channel8].angle = m2
                print ('angle: {0} \t channel: {1}'.format(m2,channel8))

        else:
            print("Error: unrecognized state for FSM1")
            
 
            
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        pass		# do nothing
