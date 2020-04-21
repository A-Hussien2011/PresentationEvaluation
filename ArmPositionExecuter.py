import ArmPositionPrediction as arm_prediction
import cv2
import time
import numpy as np


class ArmPositionExecuter:
    def __init__(self):
        self.protoFile = "pose/coco/pose_deploy_linevec.prototxt"
        self.weightsFile = "pose/coco/pose_iter_440000.caffemodel"
        self.nPoints = 18
        self.POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10], [1, 11],
                           [11, 12], [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]
        self.keypointsMapping = ['Nose', 'Neck', 'R-Sho', 'R-Elb', 'R-Wr', 'L-Sho', 'L-Elb', 'L-Wr', 'R-Hip', 'R-Knee',
                                 'R-Ank', 'L-Hip', 'L-Knee', 'L-Ank', 'R-Eye', 'L-Eye', 'R-Ear', 'L-Ear']
        self.net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsFile)
        self.threshold = 0.1
        # Empty list to store the detected keypoints
        self.points = []
        self.frame_width = 0
        self.frame_height = 0
        self.frame = None
        self.prediction = arm_prediction.ArmPositionPrediction(self.points)





    def process_new_frame(self, frame):
        self.frame = frame
        self.frame_width = frame.shape[1]
        self.frame_height = frame.shape[0]
        print(self.frame_width)
        print(self.frame_height)
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (self.frame_width, self.frame_height),
                                        (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(inpBlob)

        output = self.net.forward()
        self.extractPoints(output)
        #print(self.points)
        return self.prediction.predict_arm_position(self.points)


    def extractPoints(self, output):
        H = output.shape[2]
        W = output.shape[3]
        for i in range(self.nPoints):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            # Scale the point to fit on the original image
            x = (self.frame_width * point[0]) / W
            y = (self.frame_height * point[1]) / H

            if prob > self.threshold:
                # Add the point to the list if the probability is greater than the threshold
                self.points.append((int(x), int(y)))
            else:
                self.points.append(None)

