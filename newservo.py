import time
from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize

# Initialize PCA9685 board
kit = ServoKit(channels=16)

# Channel Definitions
channel_rotation1 = 0  # Continuous rotation servo
channel_rotation2 = 1
channel_rotation3 = 2

channel_servo1 = 12  # Normal servo (left)
channel_servo2 = 15  # Normal servo (right)

# Pulse width settings
kit.servo[channel_servo1].set_pulse_width_range(400, 2300)
kit.servo[channel_servo2].set_pulse_width_range(400, 2300)

kit.continuous_servo[channel_rotation1].set_pulse_width_range(1200, 1800)
kit.continuous_servo[channel_rotation2].set_pulse_width_range(1200, 1800)
kit.continuous_servo[channel_rotation3].set_pulse_width_range(1200, 1800)

# Default duration for test motion
duration = 2  # seconds

# Define movement functions
def move_forward():
    kit.continuous_servo[channel_rotation1].throttle = 1.0

def move_backward():
    kit.continuous_servo[channel_rotation1].throttle = -1.0

def pivot_left():
    kit.continuous_servo[channel_rotation2].throttle = -1.0
    kit.continuous_servo[channel_rotation3].throttle = 1.0

def pivot_right():
    kit.continuous_servo[channel_rotation2].throttle = 1.0
    kit.continuous_servo[channel_rotation3].throttle = -1.0

def stop():
    kit.continuous_servo[channel_rotation1].throttle = 0
    kit.continuous_servo[channel_rotation2].throttle = 0
    kit.continuous_servo[channel_rotation3].throttle = 0

# Optional: Automated demo sequence
def run_demo_sequence():
    print("Starting demo sequence.")
    try:
        for angle, speed in [(0, 1.0), (180, 0.5), (90, 0.35), (135, -1.0)]:
            kit.servo[channel_servo1].angle = angle
            kit.continuous_servo[channel_rotation1].throttle = speed
            print(f'Servo angle: {angle}, Motor speed: {speed}')
            time.sleep(duration)
        stop()
    except KeyboardInterrupt:
        print("Demo interrupted.")
        stop()

# Start gamepad control
print("Starting manual gamepad control. Press Ctrl+C to exit.")
gamepad = InputDevice('/dev/input/event9')  # Change to your actual gamepad path

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

            elif event.type == 3:  # Analog stick movement
                newstick = True
                codestick = eventinfo.event.code
                valuestick = eventinfo.event.value

        except Exception:
            continue

        # Analog stick control
        if newstick:
            if codestick == 1:  # Y-axis
                if valuestick < 100:
                    print(" ** Going Forward **")
                    move_forward()
                elif valuestick > 150:
                    print(" ** Going Backward **")
                    move_backward()
                else:
                    stop()
            elif codestick == 0:  # X-axis
                if valuestick < 100:
                    print(" ** Pivot Left **")
                    pivot_left()
                elif valuestick > 150:
                    print(" ** Pivot Right **")
                    pivot_right()
                else:
                    stop()

        # Button control
        if newbutton and valuebutton == 1:
            if codebutton == 305:
                print("Horizontal motor move")
                kit.continuous_servo[channel_rotation1].throttle = 1.0
            elif codebutton == 306:
                print("Vertical motors move")
                kit.continuous_servo[channel_rotation2].throttle = 1.0
                kit.continuous_servo[channel_rotation3].throttle = 1.0
            elif codebutton == 307:
                print("Setting servo angles to center (90 deg)")
                kit.servo[channel_servo1].angle = 90
                kit.servo[channel_servo2].angle = 90
            else:
                stop()

except KeyboardInterrupt:
    print("Manual control stopped by user.")
    stop()
    gamepad.close()

# Run demo only if needed
run_demo_sequence()
