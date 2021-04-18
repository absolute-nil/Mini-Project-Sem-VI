import cv2
import os


class WebCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.img_list = []
        self.counter = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        status, image = self.video.read()

        #Flip Image
        image_flip = cv2.flip(image, 1)

        #Crop Image
        x, y, w, h = 375, 100, 245, 260
        cv2.rectangle(image_flip, (x, y), (x + w, y + h), (0, 255, 0), 3)
        crop_img = image_flip[y:y + h, x:x + w]
        ret, jpeg = cv2.imencode('.jpg', image_flip)

        #Image Path
        path = os.getcwd() + "\camera\images" + "\image{}.jpg".format(self.counter)
        self.img_list.append(path)
        self.counter += 1
        if self.counter==10:
            self.counter=0
        #Save Image
        flipped_crop_img = cv2.flip(crop_img, 1)
        cv2.imwrite(path, flipped_crop_img)

        return jpeg.tobytes(), flipped_crop_img
