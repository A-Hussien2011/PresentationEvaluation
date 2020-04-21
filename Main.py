import time

import cv2
import imutils
from imutils.video import VideoStream

from FaceDetector import FaceDetector
from FacialExpression import FacialExpression
from MotionDetector import MotionDetector
from HeadPoseDetector import HeadPoseDetector
from ArmPoseDetector import ArmPoseDetector
from ArmPositionExecuter import ArmPositionExecuter

from ReportGenerator import ReportGenerator
from TimeFrameVideo import TimeFrameVideo

LOCAL_VIDEO = 0
REAL_TIME_VIDEO = 1
counter = 0
if __name__ == '__main__':
    video_type = input("Enter type of video: ")
    face_classifier = FacialExpression()
    motion_detector = MotionDetector()
    headpose_detector = HeadPoseDetector()
    face_detector = FaceDetector()
    arm_positon_exc = ArmPositionExecuter()

    fps = 1
    if int(video_type) == LOCAL_VIDEO:
        cap = cv2.VideoCapture('assets/videoplayback.mp4')
        fps = cap.get(cv2.CAP_PROP_FPS)
        for i in range(int(fps) * 15):
            ret, frame = cap.read()
    elif int(video_type) == REAL_TIME_VIDEO:
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)

    report = ReportGenerator()
    while True and cap.isOpened():
        timeframe = TimeFrameVideo()
        for k in range(60*2):
            # get 2 fps
            for i in range(int(fps / 2)):
                ret, frame = cap.read()
            ret, frame = cap.read()
            if frame is None:
                break
            frame = imutils.resize(frame, width=800)
            faces = face_detector.detect_face(frame)
            if len(faces) == 0:
                velocity = motion_detector.get_velocity(frame, None)
                continue
            face_exp = face_classifier.classify(frame, faces)
            velocity = motion_detector.get_velocity(frame, faces[0])
            head_pose = headpose_detector.get_head_pose(frame)
            arm_pos = arm_positon_exc.process_new_frame(frame)
            timeframe.add_expression(face_exp)
            timeframe.add_headpose(head_pose)
            if velocity is not None: timeframe.add_velocity(int(velocity))
        report.add_time_frame(timeframe)
        if frame is None:
            break
        # cv2.imshow("Video", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # cv2.waitKey(0)
        print(str(counter))
        counter += 1
    cv2.destroyAllWindows()
    report.generate_report()
