import time
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize

# === Configuration ===
kit = ServoKit(channels=16)
duration = 2  # seconds

# Channel Definitions
channel_rotation1 = 0  # Continuous rotation servo
channel_rotation2 = 1
channel_rotation3 = 2

channel_servo1 = 12  # Standard servo (left arm)
channel_servo2 = 15  # Standard servo (right arm)

# Set pulse width range for better control
kit.servo[channel_servo1].set_pulse_width_range(400, 2300)
kit.servo[channel_servo2].set_pulse_width_range(400, 2300)

kit.continuous_servo[channel_rotation1].set_pulse_width_range(1200, 1800)
kit.continuous_servo[channel_rotation2].set_pulse_width_range(1200, 1800)
kit.continuous_servo[channel_rotation3].set_pulse_width_range(1200, 1800)

# === Helper Function ===
def stop():
    kit.continuous_servo[channel_rotation1].throttle = 0
    kit.continuous_servo[channel_rotation2].throttle = 0
    kit.continuous_servo[channel_rotation3].throttle = 0

# === Gamepad Control Only ===
print("Starting manual gamepad control. Press Ctrl+C to exit.")
gamepad = InputDevice('/dev/input/event1')  # Update this path if needed

try:
    while True:
        newbutton = False
        newstick = False

        try:
            event = gamepad.read_one()
            if event is None:
                continue
            eventinfo = categorize(event)

            if event.type == 1:  # Button press
                newbutton = True
                codebutton = eventinfo.scancode
                valuebutton = eventinfo.keystate

            elif event.type == 3:  # Analog stick move
                newstick = True
                codestick = eventinfo.event.code
                valuestick = eventinfo.event.value

        except:
            continue

        if newbutton and valuebutton == 1:
            if codebutton == 305:
                # Move horizontal motor
                kit.continuous_servo[channel_rotation1].throttle = 1.0
                print(f'Horizontal move: channel {channel_rotation1}, speed 1.0')

            elif codebutton == 306:
                # Move both vertical motors
                kit.continuous_servo[channel_rotation2].throttle = 1.0
                kit.continuous_servo[channel_rotation3].throttle = 1.0
                print(f'Vertical move: channels {channel_rotation2}, {channel_rotation3}, speed 1.0')

            elif codebutton == 307:
                # Set both servos to center
                kit.servo[channel_servo1].angle = 90
                kit.servo[channel_servo2].angle = 90
                print(f'Set servos {channel_servo1}, {channel_servo2} to 90°')

            else:
                stop()

except KeyboardInterrupt:
    print("Manual control stopped by user.")
    stop()
