import time
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize, ecodes

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

# === Helper Function ===
def stop():
    print("Stopping all motors")
    kit.continuous_servo[channel_rotation1].throttle = 0
    kit.continuous_servo[channel_rotation2].throttle = 0
    kit.continuous_servo[channel_rotation3].throttle = 0


gamepad = InputDevice('/dev/input/event9')
print(gamepad)
print("")


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
'''
channel = channel_rotation1
speed = 0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))
channel = channel_rotation1
speed = -0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))
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



channel = channel_servo1
angle = 0
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  

channel = channel_servo2
angle = 90
kit.servo[channel].angle = angle
print ('angle: {0} \t channel: {1}'.format(angle,channel))  
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
channel = channel_rotation2
speed = -0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  
time.sleep(1)

channel = channel_rotation3
speed = 0.8
kit.continuous_servo[channel].throttle = speed
time.sleep(1)
print ('speed: {0} \t channel: {1}'.format(speed,channel))  
'''
