import cv2
import os


class WebCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        status, image = self.video.read()
        image_flip = cv2.flip(image, 1)
        x, y, w, h = 375, 100, 245, 260
        cv2.rectangle(image_flip, (x, y), (x + w, y + h), (0, 255, 0), 3)
        crop_img = image_flip[y:y + h, x:x + w]
        ret, jpeg = cv2.imencode('.jpg', image_flip)
        path = os.getcwd() + "\camera\images" + "\image.jpg"
        cv2.imwrite(path, crop_img)
        return jpeg.tobytes()
