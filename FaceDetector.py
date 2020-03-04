import cv2


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

    def detect_face(self, img):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        return coords
