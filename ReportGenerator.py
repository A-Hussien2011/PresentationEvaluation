import csv
import constants


class ReportGenerator:
    def __init__(self):
        self.face_count = 0
        self.vel_count = 0
        self.timeframes = []
        self.face_front = 0
        self.face_left = 0
        self.face_right = 0
        self.velocity = 0
        self.happy = 0
        self.neutral = 0
        self.other = 0

    def add_time_frame(self, timeframe):
        if (timeframe.headposes["front"] == 0 and timeframe.headposes["front"] == 0 and timeframe.headposes["front"] == 0):
            return
        self.face_count += 1
        self.face_front += timeframe.headposes["front"]
        self.face_left += timeframe.headposes["left"]
        self.face_right += timeframe.headposes["right"]
        self.happy += timeframe.expressions["happy"]
        self.neutral += timeframe.expressions["neutral"]
        self.other += timeframe.expressions["other"]
        if (timeframe.avg_velocity is not None):
            self.vel_count += 1
            self.velocity += timeframe.avg_velocity

        self.timeframes.append(timeframe)

    def generate_report(self):
        with open('assets/report.csv', 'a+', newline='') as file:
            file.seek(0)
            data = file.read(100)
            writer = csv.writer(file)
            if len(data) <= 0:
                writer.writerow(["ID", "face_front", "face_left", "face_right",
                                 "velocity", "happy", "neutral", "other_expression",
                                 "left_arm_up", "left_arm_down", "left_arm_straight", "left_arm_other",
                                 "right_arm_up", "right_arm_down", "right_arm_straight", "right_arm_other"
                                 ])

            row = []
            for i in range(len(self.timeframes)):
                row.clear()
                row.append(self.timeframes[i].name + " - " + str(i))
                row.append(self.timeframes[i].headposes["front"])
                row.append(self.timeframes[i].headposes["left"])
                row.append(self.timeframes[i].headposes["right"])
                row.append(self.timeframes[i].avg_velocity)
                row.append(self.timeframes[i].expressions["happy"])
                row.append(self.timeframes[i].expressions["neutral"])
                row.append(self.timeframes[i].expressions["other"])

                row.append(self.timeframes[i].left_armposes["up"])
                row.append(self.timeframes[i].left_armposes["down"])
                row.append(self.timeframes[i].left_armposes["straight"])
                row.append(self.timeframes[i].left_armposes["other"])

                row.append(self.timeframes[i].right_armposes["up"])
                row.append(self.timeframes[i].right_armposes["down"])
                row.append(self.timeframes[i].right_armposes["straight"])
                row.append(self.timeframes[i].right_armposes["other"])

                writer.writerow(row)
        pass

    def generate_analysis(self):
        msg = ""
        if self.face_count == 0: return

        # front face
        if constants.FRONT_MIN < (self.face_front / self.face_count) < constants.FRONT_MAX:
            msg += "Your frontal face sight is acceptable\n"
        elif (self.face_front / self.face_count) < constants.FRONT_MIN:
            msg += "You need to look more to the front\n"
        else:
            msg += "You need to look left and right more\n"

        # left face
        if constants.LEFT_MIN < (self.face_left / self.face_count) < constants.LEFT_MAX:
            msg += "Your left face sight movement is acceptable\n"
        elif (self.face_left / self.face_count) < constants.LEFT_MIN:
            msg += "You need to look more to the left\n"
        else:
            msg += "Look less to the left pay attention to the right/front side\n"

        # right face
        if constants.RIGHT_MIN < (self.face_right / self.face_count) < constants.RIGHT_MAX:
            msg += "Your frontal face movement is acceptable\n"
        elif (self.face_front / self.face_count) < constants.RIGHT_MIN:
            msg += "You need to look more to the front\n"
        else:
            msg += "You need to distribute your sight over the audience\n"

        # happy face
        if constants.HAPPY_MIN < (self.happy / self.face_count) < constants.HAPPY_MAX:
            msg += "Your happy expressions are within the acceptable range\n"
        elif (self.happy / self.face_count) < constants.HAPPY_MIN:
            msg += "You need to show more happy expressions (smile more)\n"
        else:
            msg += "You shouldn't be smiling all the time, show some other expressions to get the audience attention\n"

        if constants.NEUTRAL_MIN < (self.neutral / self.face_count) < constants.NEUTRAL_MAX:
            msg += "Your neutral face expressions are within the acceptable range\n"
        elif (self.neutral / self.face_count) < constants.NEUTRAL_MIN:
            msg += "You need to add more neutral facial expressions\n"
        else:
            msg += "Too many neutral facial expressions\n"

        if constants.OTHER_MIN < (self.other / self.face_count) < constants.OTHER_MAX:
            msg += "Your other facial expression  are within the acceptable range\n"
        elif (self.other / self.face_count) < constants.OTHER_MIN:
            msg += "You need to show more facial expressions rather than only smiles/neutral\n"
        else:
            msg += "Show less other expressions(Sadness - anger - disgust .. etc)\n"

        if self.vel_count == 0:
            msg += "No velocity for your movement could be determined"
        elif constants.VELOCITY_MIN < (self.velocity / self.vel_count) < constants.VELOCITY_MAX:
            msg += "The velocity of your movement is acceptable\n"
        elif (self.velocity / self.vel_count) < constants.VELOCITY_MIN:
            msg += "Move more to have better interaction with the audience\n"
        else:
            msg += "You need to move less not to disturb the audience\n"

        with open('assets/' + self.timeframes[0].name + '.txt', 'a+', newline='') as file:
            file.write(msg)
