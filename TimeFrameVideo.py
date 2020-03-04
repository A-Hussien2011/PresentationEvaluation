class TimeFrameVideo:
    def __init__(self):
        self.expressions = {'happy': 0, 'neutral': 0, 'other': 0}
        self.headposes = {'front': 0, 'left': 0, 'right': 0}
        self.avg_velocity = None
        self.velocities = []

    def add_expression(self, current_exp):
        for key in current_exp:
            self.expressions[key] += current_exp[key]

    def add_velocity(self, velocity):
        self.velocities.append(velocity)
        self.avg_velocity = sum(self.velocities)/len(self.velocities)

    def add_headpose(self, current_headpose):
        for key in current_headpose:
            self.headposes[key] += current_headpose[key]

    def add_armpose(self):
        pass