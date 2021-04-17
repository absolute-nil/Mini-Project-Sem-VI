from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from camera.camera_helper import WebCam
import time

def index(request):
	context = {'switch':False}
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
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	

def video_feed(request):
	return StreamingHttpResponse(gen(WebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def tester(request):
	return render(request, 'tester.html')
	#saved_model = tf.keras.models.load_model('Alphabet Classifier With Preprocessing')