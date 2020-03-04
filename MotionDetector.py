import timeit
import numpy as np
import cv2

class MotionDetector:
    def __init__(self):
        self.initBB = None
        self.center = [0, 0]
        self.t_start = 0
        (major, minor) = cv2.__version__.split(".")[:2]
        if int(major) == 3 and int(minor) < 3:
            self.tracker = cv2.Tracker_create("CSRT")
        else:
            self.tracker = cv2.TrackerCSRT_create()

    def get_velocity(self, frame, face):
        if frame is None:
            return None
        if face is None:
            self.initBB = None
            return None
        if self.initBB is None and face is not None:
            face = tuple(face)
            self.initBB = face
            self.center = (face[0] + face[2] / 2, face[1] + face[3] / 2)
            self.tracker.init(frame, self.initBB)
            return None

        (H, W) = frame.shape[:2]
        if self.initBB is not None:
            (success, box) = self.tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                newCenter = (x + w / 2, y + h / 2)
                # t_end = timeit.timeit()
                velocity = [0, 0]
                #2 frames per second
                velocity[0] = abs(newCenter[0] - self.center[0])/0.5
                velocity[1] = abs(newCenter[1] - self.center[1])/0.5
                vel = np.math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
                self.center = newCenter
                return vel