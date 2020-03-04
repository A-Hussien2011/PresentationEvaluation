import cv2
import dlib


class HeadPoseDetector:

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("assets/headPose/shape_predictor_68_face_landmarks.dat")

    def get_direction(self, landmarks):
        left = landmarks.part(1)
        right = landmarks.part(16)
        # up = landmarks.part(16)
        # down = landmarks.part(16)
        nose = landmarks.part(29)
        direction = "front"
        difference = abs(nose.x - left.x) - abs(nose.x - right.x)
        if -20 < difference < 20:
            direction = "front"
        elif difference < 0:
            direction = "left"
        else:
            direction = "right"
        return direction

    def get_head_pose(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        # directions = {'front': 0, 'left': 0, 'right': 0, 'down': 0, 'up': 0}
        directions = {'front': 0, 'left': 0, 'right': 0}
        for face in faces:
            landmarks = self.predictor(gray, face)
            direction = self.get_direction(landmarks)
            directions[direction] += 1
        return directions
