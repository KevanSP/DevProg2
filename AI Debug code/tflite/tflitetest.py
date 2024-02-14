from time import sleep
import numpy as np
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter

# Path to the TFLite model
modelPath = 'model_unquant.tflite'

# Path to the labels file
labelPath = 'labels.txt'


# This function takes in a TFLite Interpreter and Image, and returns classifications
def classifyImage(interpreter, image):
    input_details = interpreter.get_input_details()
    expected_shape = input_details[0]['shape']  # Get expected input shape

    # Check if reshaping is needed based on expected shape
    if image.size != (expected_shape[2], expected_shape[1]):
        image = image.resize((expected_shape[2], expected_shape[1]))

    # Preprocess the input image
    input_data = np.array(image.convert('RGB'), dtype=np.float32)
    input_data = (input_data / 127.5) - 1.0  # Normalize pixel values
    input_data = np.expand_dims(input_data, axis=0)  # Add batch dimension

    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output results
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data


def main():
    # Start Camera
    picam2 = Picamera2()
    picam2.start()
    sleep(1)
    # Load your model onto the TF Lite Interpreter
    interpreter = Interpreter(modelPath)
    interpreter.allocate_tensors()

    labels = []
    with open(labelPath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Replace this with your image loading logic
    # For example, you can use the PIL library to open an image file
    # image_path = 'test_image.jpg'
    # image = Image.open(image_path)
    image = picam2.capture_image("main")

    # Classify and display image
    results = classifyImage(interpreter, image)
    predicted_index = np.argmax(results[0])
    print(f'Label: {labels[predicted_index]}, Score: {results[0][predicted_index]}')


if __name__ == '__main__':
    main()
