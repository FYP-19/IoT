import RPi.GPIO as GPIO
import subprocess
import time
import os
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin for the switch
switch_pin = 23
# Set up GPIO pin as input with pull-up resistor
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Counter for captured images
image_count = 0

# Define the directory to save images
image_directory = "/home/fyp-19/images"

# Ensure the directory exists
os.makedirs(image_directory, exist_ok=True)

# Function to run the script when the switch is pressed
def switch_callback(channel):
    global image_count
    global predictions_list
    model_path = '/home/fyp-19/models/mobilenetv2.tflite'
    labels_path = '/home/fyp-19/scripts/labels.txt'
    
    # Capture three images using raspistill
    for i in range(3):
        image_count += 1
        image_filename = f"{image_directory}/image_{image_count}.jpg"
        subprocess.run(["raspistill", "-o", image_filename])
        print(f"Image captured: {image_filename}")

        # Load the TensorFlow Lite model
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()

        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Load and preprocess the captured image
        image = Image.open(image_filename).resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
        input_data = np.expand_dims(image, axis=0)
        input_data = (np.float32(input_data) - 127.5) / 127.5  # Normalize the input

        # Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # Load labels from a file (Assuming labels are stored in a txt file)
        
        with open(labels_path, 'r') as f:
            labels = f.read().splitlines()

        # Process the output to get predictions
        decoded_predictions = np.argmax(output_data, axis=1)
        predicted_label = labels[decoded_predictions[0]]
        print(f"Predicted class label for Image {image_count}: {predicted_label}")

        # Store the predicted label in the list
        predictions_list.append(predicted_label)

# Add event detection for button press
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_callback, bouncetime=5000)

# List to store predicted labels
predictions_list = []

try:
    print("Switch listener is running. Press Ctrl+C to exit.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Print the predicted labels for each image
    if predictions_list:
        for i, label in enumerate(predictions_list):
            print(f"Image {i + 1} predicted label: {label}")

    print("Exiting...")

finally:
    GPIO.cleanup()
