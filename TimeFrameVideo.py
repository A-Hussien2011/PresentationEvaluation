class TimeFrameVideo:
    def __init__(self):
        self.expressions = {'happy': 0, 'neutral': 0, 'other': 0}
        self.headposes = {'front': 0, 'left': 0, 'right': 0}
        self.left_armposes = {'up': 0, 'down': 0, 'straight': 0, "other": 0}
        self.right_armposes = {'up': 0, 'down': 0, 'straight': 0, "other": 0}
        self.avg_velocity = None
        self.velocities = []
        self.name = ""

    def add_expression(self, current_exp):
        for key in current_exp:
            self.expressions[key] += current_exp[key]

    def add_velocity(self, velocity):
        self.velocities.append(velocity)
        self.avg_velocity = sum(self.velocities) / len(self.velocities)

    def add_headpose(self, current_headpose):
        for key in current_headpose:
            self.headposes[key] += current_headpose[key]

    def add_armpose(self, armposes):
        right_label = self.get_armpose_label(armposes[0])
        left_label = self.get_armpose_label(armposes[1])
        self.right_armposes[right_label] += 1
        self.left_armposes[left_label] += 1
        pass

    def get_armpose_label(self, arr):
        if arr == [1, 0, 0, 0, 0, 0, 0, 0, 0]:
            return "up"
        elif arr == [0, 1, 0, 0, 0, 0, 0, 0, 0]:
            return "down"
        elif arr == [0, 0, 1, 0, 0, 0, 0, 0, 0]:
            return "straight"
        else:
            return "other"

    def set_name(self, filename):
        self.name = filename
