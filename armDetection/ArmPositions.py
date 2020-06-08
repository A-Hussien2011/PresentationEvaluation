import enum


# Using enum class create enumerations


class ArmPositions(enum.Enum):
    UP = 1
    DOWN = 2
    STRAIGHT = 3
    FLASHING = 4
    FRONT_UP = 5
    FRONT_DOWN = 6
    FRONT_CENTER = 7
    STRAIGHT_UP = 8
    STRAIGHT_DOWN = 9


# Hashing to create a dictionary


arm_gesture_type = {}

#                   *
#                   |
# Arm is up     + --|
arm_gesture_type[ArmPositions.UP] = [1, 0, 0, 0, 0, 0, 0, 0, 0]
# Arm is down   +--|
#                  |
#                  *
arm_gesture_type[ArmPositions.DOWN] = [0, 1, 0, 0, 0, 0, 0, 0, 0]

# Arm is straight    |--+--|------>
arm_gesture_type[ArmPositions.STRAIGHT] = [0, 0, 1, 0, 0, 0, 0, 0, 0]

# Arm is not appear in the frame X
arm_gesture_type[ArmPositions.FLASHING] = [0, 0, 0, 1, 0, 0, 0, 0, 0]

# Arm is front of the center and up         +\--|
#                                             \_|
arm_gesture_type[ArmPositions.FRONT_UP] = [0, 0, 0, 0, 1, 0, 0, 0, 0]
# Arm is front of the center and down        +--|
#                                               |
#                                              /
#                                            /
arm_gesture_type[ArmPositions.FRONT_DOWN] = [0, 0, 0, 0, 0, 1, 0, 0, 0]
# Arm is front of the center and bow is straight        +--|
#                                                      ____|

arm_gesture_type[ArmPositions.FRONT_CENTER] = [0, 0, 0, 0, 0, 0, 1, 0, 0]
#                                            /
#                                           /
# Arm is between up and straight    ---+---/
arm_gesture_type[ArmPositions.STRAIGHT_UP] = [0, 0, 0, 0, 0, 0, 0, 1, 0]

# Arm is between down and straight  ---+---\
#                                           \
#                                            \
arm_gesture_type[ArmPositions.STRAIGHT_DOWN] = [0, 0, 0, 0, 0, 0, 0, 0, 1]

# Checking if the hashing is successful
#print(arm_gesture_type == {ArmPositions.UP: [1, 0, 0, 0, 0, 0, 0, 0, 0], ArmPositions.DOWN: [0, 1, 0, 0, 0, 0, 0, 0, 0]})


def get_arm_gesture_type(type):
    return arm_gesture_type[type]