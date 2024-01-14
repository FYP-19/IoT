import RPi.GPIO as GPIO
import subprocess
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin for the switch
switch_pin = 23 
# Set up GPIO pin as input with pull-up resistor
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to run the script when the switch is pressed
def switch_callback(channel):
    print("Switch pressed!")
    subprocess.run(["python", "run_model.py"])


GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_callback, bouncetime=300)

try:
    print("Switch listener is running. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
