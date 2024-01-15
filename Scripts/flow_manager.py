import RPi.GPIO as GPIO
import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin for the switch
switch_pin = 23
# Set up GPIO pin as input with pull-up resistor
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to run the script when the switch is pressed
def switch_callback(channel):
    print("Switch pressed!")

    # Load the TensorFlow Lite model
    model_path = '/home/fyp/fyp-19/models/mobilenetv2.tflite'
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load and preprocess the image
    image_path = '/home/fyp/fyp-19/images/pig.jpg'  # Update with your image path
    image = Image.open(image_path).resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
    input_data = np.expand_dims(image, axis=0)
    input_data = (np.float32(input_data) - 127.5) / 127.5  # Normalize the input

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Load labels
    labels_path = '/home/fyp/fyp-19/scripts/labels.txt' 
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # Process the output to get predictions
    decoded_predictions = np.argmax(output_data, axis=1)
    predicted_label = labels[decoded_predictions[0]]
    print("Predicted class label:", predicted_label)

# Add event detection for the falling edge (switch press)
GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=switch_callback, bouncetime=5000)

try:
    print("Switch listener is running. Press Ctrl+C to exit.")
    while True:
        pass  

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()
