from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from camera.camera_helper import WebCam
import time
import tensorflow as tf
import numpy as np
import cv2
import os

SIZE = 64, 64
PATH = os.getcwd() + r"\camera\Alphabet_Classifier__Preprocess_Lite.tflite"
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(PATH)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

predictedCharacter = ''
predictedString = ''

def index(request):
	context = {'switch': False}
	if request.method=='GET':
		if 'btn' in request.GET:
			switch = request.GET['btn']
			if switch=='turn-on':
				context['switch'] = True
	return render(request, 'index.html', context)

def gen(camera):
	end_time = time.time() + 5
	while time.time() < end_time:
		frame = camera.get_frame()
		print(prediction(frame))
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	return redirect('index.html')
	

def video_feed(request):
	return StreamingHttpResponse(gen(WebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def tester(request):
	return render(request, 'tester.html?btn=turn-off')

def prediction(image):
	
	#Preprocessing
	resizedImage = cv2.resize(image, SIZE)
	input_data = np.array(resizedImage, dtype = np.float32)
	input_data = input_data[np.newaxis, ...]
	interpreter.set_tensor(input_details[0]['index'], input_data)

	interpreter.invoke()

	# The function `get_tensor()` returns a copy of the tensor data.
	# Use `tensor()` in order to get a pointer to the tensor.
	output_data = interpreter.get_tensor(output_details[0]['index'])
	index = np.argmax(output_data, axis = -1)
	prediction = chr(ord('A') + index)
	
	return prediction
