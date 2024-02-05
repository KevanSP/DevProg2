from PIL import Image
from tflite_runtime.interpreter import Interpreter

# Path to the TFLite model
modelPath = '<PATH_TO_MODEL>'

# Path to the labels file
labelPath = '<PATH_TO_LABELS>'

# This function takes in a TFLite Interpreter and Image, and returns classifications
def classifyImage(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocess the input image
    input_data = image.resize((input_details[0]['shape'][2], input_details[0]['shape'][1])).convert('RGB')
    input_data = list(input_data.getdata())
    input_data = [[(pixel[0] / 127.5) - 1.0, (pixel[1] / 127.5) - 1.0, (pixel[2] / 127.5) - 1.0] for pixel in input_data]
    input_data = [item for sublist in input_data for item in sublist]
    input_data = [input_data]

    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the output results
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    return output_data

def main():
    # Load your model onto the TF Lite Interpreter
    interpreter = Interpreter(modelPath)
    interpreter.allocate_tensors()

    labels = []
    with open(labelPath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Replace this with your image loading logic
    # For example, you can use the PIL library to open an image file
    image_path = '<PATH_TO_IMAGE>'
    image = Image.open(image_path)

    # Classify and display image
    results = classifyImage(interpreter, image)
    print(f'Label: {labels[results[0][0]]}, Score: {results[0][1]}')

if __name__ == '__main__':
    main()