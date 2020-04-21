import ArmPositions as armp


class ArmPositionPrediction:
    # init method or constructor
    def __init__(self, points):
        self.points = points

    # 1
    def up_arm_prediction(self, type):
        return False

    # 2
    def down_arm_prediction(self, type):
        return True

    # 3
    def straight_arm_prediction(self, type):
        return True

    # 4
    def flashing_arm_prediction(self, type):
        return True

    # 5
    def front_up_arm_prediction(self, type):
        return True

    # 6
    def front_down_arm_prediction(self, type):
        return True

    # 7
    def front_center_arm_prediction(self, type):
        return True

    # 8
    def straight_up_arm_prediction(self, type):
        return True

    # 9
    def straight_down_arm_prediction(self, type):
        return True

    def predict_arm_position(self, points):
        two_arm_pos = [self.left_hand_Pos_pred(points), self.right_hand_Pos_pred(points)]
        return two_arm_pos

    def left_hand_Pos_pred(self, points):
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

    def right_hand_Pos_pred(self, points):
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
