import timeit
import numpy as np
import cv2

class MotionDetector:
    def __init__(self):
        self.master = None
        self.disp = [0, 0]
        self.velocity = [0, 0]
        self.t_start = 0
        self.t_end = 0

    def get_targets(self, contours):
        targets = []
        for c in contours:
            if cv2.contourArea(c) < 500:
                continue
            M = cv2.moments(c)  # ;print( M )
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(c)
            ca = cv2.contourArea(c)
            targets.append((cx, cy, ca))
        return targets

    def get_center(self, targets):
        mx = 0
        my = 0
        if targets:
            area = 0
            for x, y, a in targets:
                mx += x * a
                my += y * a
                area += a
            mx = int(round(mx / area, 0))
            my = int(round(my / area, 0))
        return mx, my

    def get_velocity(self, frame0):
        self.t_end = timeit.timeit()
        frame1 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        frame2 = cv2.GaussianBlur(frame1, (15, 15), 0)
        if self.master is None:
            self.master = frame2
            self.t_start = self.t_end
            return 0
        frame3 = cv2.absdiff(self.master, frame2)
        frame4 = cv2.threshold(frame3, 80, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((2, 2), np.uint8)
        frame5 = cv2.erode(frame4, kernel, iterations=4)
        frame5 = cv2.dilate(frame5, kernel, iterations=8)
        contours, _ = cv2.findContours(frame5.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # frame6 = frame0.copy()
        targets = self.get_targets(contours)
        (mx, my) = self.get_center(targets)
        self.velocity[0] = abs(mx - self.disp[0]) / (self.t_end - self.t_start)
        self.velocity[1] = abs(my - self.disp[1]) / (self.t_end - self.t_start)
        vel = np.math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)
        self.disp[0] = mx
        self.disp[1] = my
        self.master = frame2
        self.t_start = self.t_end
        return vel