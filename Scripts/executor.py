import RPi.GPIO as GPIO
import subprocess
import time
import os

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin for the switch
switch_pin = 23
# Set up GPIO pin as input with pull-up resistor
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Counter for captured images
image_count = 0

# Define the directory to save images
image_directory = "/home/fyp/fyp-19/images"

# Ensure the directory exists
os.makedirs(image_directory, exist_ok=True)

# Function to run the script when the switch is pressed
def switch_callback(channel):
    global image_count
    print("Switch pressed!")

    # Capture three images using raspistill
    for i in range(3):
        image_count += 1
        image_filename = f"{image_directory}/image_{image_count}.jpg"
        subprocess.run(["raspistill", "-o", image_filename])
        print(f"Image captured: {image_filename}")

# Add event detection for button press
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_callback, bouncetime=300)

try:
    print("Switch listener is running. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
