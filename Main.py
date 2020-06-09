import cv2
import imutils
import os

from FaceDetector import FaceDetector
from FacialExpression import FacialExpression
from MotionDetector import MotionDetector
from HeadPoseDetector import HeadPoseDetector
from armDetection.ArmPositionExecuter import ArmPositionExecuter

from ReportGenerator import ReportGenerator
from TimeFrameVideo import TimeFrameVideo

LOCAL_VIDEO = 0
REAL_TIME_VIDEO = 1


def startVideoAnalysis(path):
    video_type = LOCAL_VIDEO
    face_classifier = FacialExpression()
    motion_detector = MotionDetector()
    headpose_detector = HeadPoseDetector()
    face_detector = FaceDetector()
    arm_positon_exc = ArmPositionExecuter()

    fps = 1
    if int(video_type) == LOCAL_VIDEO:
        cap = cv2.VideoCapture(path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        for i in range(int(fps) * 15):
            ret, frame = cap.read()
    elif int(video_type) == REAL_TIME_VIDEO:
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)

    report = ReportGenerator()
    while True and cap.isOpened():
        timeframe = TimeFrameVideo()
        pathSplits = path.split('/')
        timeframe.set_name(pathSplits[len(pathSplits) - 1])
        for k in range(60 * 2):
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
            arm_pose = arm_positon_exc.process_new_frame(frame)
            timeframe.add_armpose(arm_pose)
            timeframe.add_expression(face_exp)
            timeframe.add_headpose(head_pose)
            if velocity is not None: timeframe.add_velocity(int(velocity))
        report.add_time_frame(timeframe)
        if frame is None:
            break
    cv2.destroyAllWindows()
    report.generate_report()


if __name__ == '__main__':
    for file in os.listdir("/content/drive/My Drive/Graduation project/TedTalks"):
        if file.endswith(".mp4"):
            path = os.path.join("/content/PresentationEvaluation/assets/videos/TedTalks", file)
            print(path)
            startVideoAnalysis(path)
            os.remove(path)
