from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from camera.camera_helper import WebCam
import time

def index(request):
    return render(request, 'index.html')

def gen(camera):
	end_time = time.time() + 5
	while time.time() < end_time:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	

def video_feed(request):
	return StreamingHttpResponse(gen(WebCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')