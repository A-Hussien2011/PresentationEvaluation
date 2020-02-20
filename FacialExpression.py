import cv2
import numpy as np
from IPython.utils import frame
from keras_preprocessing.image import img_to_array
from tensorflow.python.keras.models import load_model, model_from_json


class FacialExpression:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')
        self.exp_model = model_from_json(open("assets/facialExpressions/facialModel.json", "r").read())
        self.exp_model.load_weights('assets/facialExpressions/facial_expression_model_weights.h5')

    def predict_exp(self, detected_face):
        emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # transform to gray scale
        detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48
        img_pixels = img_to_array(detected_face)
        img_pixels = np.expand_dims(img_pixels, axis=0)
        img_pixels /= 255
        predictions = self.exp_model.predict(img_pixels)
        max_index = np.argmax(predictions[0])
        return emotions[max_index]

    def detect_faces(self, img):
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
        return coords

    def classify(self, frame):
        detections = self.detect_faces(frame)
        predictions = {'happy': 0, 'neutral': 0, 'other': 0}
        for i in range(0, len(detections)):
            (startX, startY, w, h) = detections[i]
            endX = startX + w
            endY = startY + h
            detected_face = frame[startY:endY, startX:endX]
            prediction = self.predict_exp(detected_face)
            if prediction == 'happy' or prediction == 'neutral':
                predictions[prediction] += 1
            else:
                predictions['other'] += 1
        return predictions