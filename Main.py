import cv2
import imutils
from imutils.video import VideoStream

from FacialExpression import FacialExpression
from MotionDetector import MotionDetector
from HeadPoseDetector import HeadPoseDetector
from ArmPoseDetector import ArmPoseDetector

LOCAL_VIDEO = 0
REAL_TIME_VIDEO = 1

if __name__ == '__main__':
    video_type = input("Enter type of video: ")
    face_classifier = FacialExpression()
    motion_detector = MotionDetector()
    headpose_detector = HeadPoseDetector()
    if int(video_type) == LOCAL_VIDEO:
        pass
    elif int(video_type) == REAL_TIME_VIDEO:
        vs = VideoStream(src=0).start()
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=800)
            cv2.imshow("Video", frame)
            face_exp = face_classifier.classify(frame)
            velocity = motion_detector.get_velocity(frame)
            head_pose = headpose_detector.get_head_pose(frame)
            print(face_exp.__str__())
            print(velocity)
            print(head_pose.__str__())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.waitKey(0)
        cv2.destroyAllWindows()
