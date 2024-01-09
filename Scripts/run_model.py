import numpy as np
import PIL
from PIL import Image
import tflite_runtime.interpreter as tflite

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

# Load labels from a file (Assuming labels are stored in a txt file)
labels_path = '/home/fyp/fyp-19/scripts/labels.txt'  # Update with your label file path
with open(labels_path, 'r') as f:
    labels = f.read().splitlines()

# Process the output to get predictions
decoded_predictions = np.argmax(output_data, axis=1)
predicted_label = labels[decoded_predictions[0]]
print("Predicted class label:", predicted_label)
