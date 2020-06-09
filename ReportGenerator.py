import csv


class ReportGenerator:
    def __init__(self):
        self.count = 0
        self.timeframes = []

    def add_time_frame(self, timeframe):
        self.count += 1
        self.timeframes.append(timeframe)

    def generate_report(self):
        with open('/content/drive/My Drive/Graduation project/assets/report.csv', 'a+', newline='') as file:
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
