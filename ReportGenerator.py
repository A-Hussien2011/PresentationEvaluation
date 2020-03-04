import csv


class ReportGenerator:
    def __init__(self):
        self.count = 0
        self.timeframes = []

    def add_time_frame(self, timeframe):
        self.count += 1
        self.timeframes.append(timeframe)

    def generate_report(self):
        with open('assets/report.csv', 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "front", "left", "right", "velocity", "happy", "neutral", "other"])
            row = []
            for i in range(len(self.timeframes)):
                row.clear()
                row.append(i)
                row.append(self.timeframes[i].headposes["front"])
                row.append(self.timeframes[i].headposes["left"])
                row.append(self.timeframes[i].headposes["right"])
                row.append(self.timeframes[i].avg_velocity)
                row.append(self.timeframes[i].expressions["happy"])
                row.append(self.timeframes[i].expressions["neutral"])
                row.append(self.timeframes[i].expressions["other"])
                writer.writerow(row)
        pass
