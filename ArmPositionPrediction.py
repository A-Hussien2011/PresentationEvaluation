import ArmPositions as armp
import math
from AngleCalculator import AngleCalculator


class ArmPositionPrediction:
    # init method or constructor
    def __init__(self, points):
        self.points = points
        self.angle_cal = AngleCalculator()
        self.key_points_mapping = {"Nose": 0, "Neck": 1, "R-Sho": 2, "R-Elb": 3, "R-Wr": 4, "L-Sho": 5, "L-Elb": 6,
                                   "L-Wr": 7, "R-Hip": 8, "R-Knee": 9, "R-Ank": 10, "L-Hip": 11, "L-Knee": 12,
                                   "L-Ank": 13, "R-Eye": 14, "L-Eye": 15, "R-Ear": 17, "L-Ear": 18}
        self.hip_center = None  # point 8 11
        self.backbone_center = None  # point 1 & hip_center

        self.neck_to_left_wrist_dis = -1
        self.hip_to_left_wrist_dis = -1
        self.center_to_left_wrist_dis = -1

        self.left_arm_angle1 = -1  # point 1 , 5 ,6
        self.left_arm_angle2 = -1  # point 5, 6 , 7

        self.neck_to_right_wrist_dis = -1
        self.hip_to_right_wrist_dis = -1
        self.center_to_right_wrist_dis = -1

        self.right_arm_angle1 = -1  # point 1 2 3
        self.right_arm_angle2 = -1  # points 2 3 4

    def predict_arm_position(self, points):
        self.points = points
        self.set_measurement()
        two_arm_pos = [self.right_hand_Pos_pred(), self.left_hand_Pos_pred()]
        return two_arm_pos

    # 1
    def up_arm_prediction(self, type):
        if type == "L":
            if 80 <= self.left_arm_angle1 <= 120:
                if self.neck_to_left_wrist_dis != -1 and self.hip_to_left_wrist_dis != -1:
                    if self.neck_to_left_wrist_dis < self.hip_to_left_wrist_dis:
                        return True
        if type == "R":
            if 80 <= self.right_arm_angle1 <= 120:
                if self.neck_to_right_wrist_dis != -1 and self.hip_to_right_wrist_dis != -1:
                    if self.neck_to_right_wrist_dis < self.hip_to_right_wrist_dis:
                        return True
        return False

    # 2
    def down_arm_prediction(self, type):
        if type == "L":
            if 80 <= self.left_arm_angle1 <= 120:
                if self.neck_to_left_wrist_dis != -1 and self.hip_to_left_wrist_dis != -1:
                    if self.neck_to_left_wrist_dis > self.hip_to_left_wrist_dis:
                        return True
        if type == "R":
            if 80 <= self.right_arm_angle1 <= 120:  # range 9
                if self.neck_to_right_wrist_dis != -1 and self.hip_to_right_wrist_dis != -1:
                    if self.neck_to_right_wrist_dis > self.hip_to_left_wrist_dis:
                        return True
        return False

    # 3
    def straight_arm_prediction(self, type):
        if type == "L":
            if 135 < self.left_arm_angle1 <= 180:
                if 135 < self.left_arm_angle2 <= 180:
                    return True
                else:
                    return True
        if type == "R":
            if 135 < self.right_arm_angle1 <= 180:  # range 9
                if 135 < self.right_arm_angle2 <= 180:
                    return True
                else:
                    return True
        return False

    # 4
    def flashing_arm_prediction(self, type):
        if type == "L":
            if self.left_arm_angle1 == -1:
                return True
        if type == "R":
            if self.right_arm_angle1 == -1:
                return True
        return False

    # 5
    def front_up_arm_prediction(self, type):
        if type == "L":
            if 80 <= self.left_arm_angle1 <= 100:
                if self.center_to_left_wrist_dis < self.neck_to_left_wrist_dis:
                    return True
        if type == "R":
            if 80 <= self.right_arm_angle1 <= 100:
                if self.center_to_right_wrist_dis < self.center_to_right_wrist_dis:
                    return True
        return False

    # 6
    def front_down_arm_prediction(self, type):
        if type == "L":
            if 80 <= self.left_arm_angle1 <= 100:
                if self.center_to_left_wrist_dis < self.hip_to_left_wrist_dis:
                    return True
        if type == "R":
            if 80 <= self.right_arm_angle1 <= 100:
                if self.center_to_left_wrist_dis < self.hip_to_right_wrist_dis:
                    return True
        return False

    # 7
    def front_center_arm_prediction(self, type):
        if type == "L":
            if 80 <= self.left_arm_angle1 <= 120:
                return True
        if type == "R":
            if 80 <= self.right_arm_angle1 <= 120:
                return True
        return False

    # 8
    def straight_up_arm_prediction(self, type):
        if type == "L":
            if 120 < self.left_arm_angle1 <= 180:
                if self.neck_to_left_wrist_dis != -1 and self.backbone_center is not None:
                    if self.hip_to_left_wrist_dis > self.neck_to_left_wrist_dis:
                        return True
                else:
                    return True
        if type == "R":
            if 120 < self.right_arm_angle1 <= 180:  # range 9
                if self.neck_to_right_wrist_dis != -1 and self.hip_to_right_wrist_dis != -1:
                    if self.hip_to_right_wrist_dis > self.neck_to_right_wrist_dis:
                        return True
                else:
                    return True
        return False

    # 9
    def straight_down_arm_prediction(self, type):
        if type == "L":
            if 120 < self.left_arm_angle1 <= 180:
                if self.neck_to_left_wrist_dis != -1 and self.backbone_center is not None:
                    if self.hip_to_left_wrist_dis < self.neck_to_left_wrist_dis:
                        return True
                else:
                    return True
        if type == "R":
            if 120 < self.right_arm_angle1 <= 180:  # range 9
                if self.neck_to_right_wrist_dis != -1 and self.hip_to_right_wrist_dis != -1:
                    if self.hip_to_right_wrist_dis < self.neck_to_right_wrist_dis:
                        return True
                else:
                    return True
        return False

    def left_hand_Pos_pred(self):
        if self.flashing_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FLASHING)
        if self.up_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.UP)
        if self.down_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.DOWN)
        if self.straight_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT)
        if self.straight_down_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT_DOWN)
        if self.straight_up_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT_UP)
        if self.front_down_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_DOWN)
        if self.front_up_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_UP)
        if self.front_center_arm_prediction("L"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_CENTER)
        return None

    def right_hand_Pos_pred(self):
        if self.flashing_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FLASHING)
        if self.up_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.UP)
        if self.down_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.DOWN)
        if self.straight_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT)
        if self.straight_down_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT_DOWN)
        if self.straight_up_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.STRAIGHT_UP)
        if self.front_down_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_DOWN)
        if self.front_up_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_UP)
        if self.front_center_arm_prediction("R"):
            return armp.get_arm_gesture_type(armp.ArmPositions.FRONT_CENTER)
        return None

    def set_measurement(self):
        self.set_dis_to_neck()
        self.set_dis_to_hip()
        self.set_dis_to_center()

        self.set_angles()

    def set_dis_to_neck(self):
        if self.points[self.key_points_mapping["Neck"]] is not None:
            if self.points[self.key_points_mapping["R-Wr"]] is not None:
                self.neck_to_right_wrist_dis = self.dis(self.points[self.key_points_mapping["R-Wr"]],
                                                        self.points[self.key_points_mapping["Neck"]])
            if self.points[self.key_points_mapping["L-Wr"]] is not None:
                self.neck_to_left_wrist_dis = self.dis(self.points[self.key_points_mapping["L-Wr"]],
                                                       self.points[self.key_points_mapping["Neck"]])

    def set_dis_to_hip(self):
        if self.points[self.key_points_mapping["R-Hip"]] is not None and self.points[
            self.key_points_mapping["L-Hip"]] is not None:
            self.hip_center = self.midpoint(self.points[self.key_points_mapping["R-Hip"]],
                                            self.points[self.key_points_mapping["L-Hip"]])

            if self.points[self.key_points_mapping["Neck"]] is not None:
                self.backbone_center = self.midpoint(self.hip_center, self.points[self.key_points_mapping["Neck"]])

            if self.points[self.key_points_mapping["R-Wr"]] is not None:
                self.hip_to_right_wrist_dis = self.dis(self.points[self.key_points_mapping["R-Wr"]], self.hip_center)

            if self.points[self.key_points_mapping["L-Wr"]] is not None:
                self.hip_to_left_wrist_dis = self.dis(self.points[self.key_points_mapping["L-Wr"]], self.hip_center)

    def set_dis_to_center(self):
        if self.backbone_center is not None:
            if self.points[self.key_points_mapping["R-Wr"]] is not None:
                self.center_to_right_wrist_dis = self.dis(self.points[self.key_points_mapping["R-Wr"]],
                                                          self.backbone_center)
                print("center_to_right_wrist_dis = " + str(self.center_to_right_wrist_dis))

            if self.points[self.key_points_mapping["L-Wr"]] is not None:
                self.center_to_left_wrist_dis = self.dis(self.points[self.key_points_mapping["L-Wr"]],
                                                         self.backbone_center)
                print("center_to_left_wrist_dis = " + str(self.center_to_left_wrist_dis))

    def set_angles(self):
        self.set_right_hand_angles()
        self.set_left_hand_angles()

    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

    def dis(self, x, y):
        return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    def set_right_hand_angles(self):
        p = self.points
        if p[self.key_points_mapping["R-Wr"]] is not None:
            if p[self.key_points_mapping["R-Elb"]] is not None:
                if p[self.key_points_mapping["R-Sho"]] is not None:
                    self.right_arm_angle2 = self.angle_cal.get_angle(p[self.key_points_mapping["R-Wr"]],
                                                                     p[self.key_points_mapping["R-Elb"]],
                                                                     p[self.key_points_mapping["R-Sho"]])
                    print("right arm angle 2 = " + str(self.right_arm_angle2))
                    self.right_arm_angle1 = self.angle_cal.get_angle(p[self.key_points_mapping["R-Elb"]],
                                                                     p[self.key_points_mapping["R-Sho"]],
                                                                     p[self.key_points_mapping["Neck"]])
                    print("right arm angle  1 = " + str(self.right_arm_angle1))


    def set_left_hand_angles(self):
        p = self.points
        if p[self.key_points_mapping["L-Wr"]] is not None:
            if p[self.key_points_mapping["L-Elb"]] is not None:
                if p[self.key_points_mapping["L-Sho"]] is not None:
                    self.left_arm_angle2 = self.angle_cal.get_angle(p[self.key_points_mapping["L-Wr"]],
                                                                    p[self.key_points_mapping["L-Elb"]],
                                                                    p[self.key_points_mapping["L-Sho"]])
                    print("Left arm angle 2 = " + str(self.left_arm_angle2))
                    self.left_arm_angle1 = self.angle_cal.get_angle(p[self.key_points_mapping["L-Elb"]],
                                                                    p[self.key_points_mapping["L-Sho"]],
                                                                    p[self.key_points_mapping["Neck"]])
                    print("Left arm angle 1 = " + str(self.left_arm_angle1))
