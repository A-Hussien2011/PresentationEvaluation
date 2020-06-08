import math
import numpy as np


class AngleCalculator:
    def __init__(self):
       pass
    # returns square of distance b/w two points
    def length_square(self,X, Y):
        x_diff = X[0] - Y[0]
        y_diff = X[1] - Y[1]
        return x_diff * x_diff + y_diff * y_diff

    def get_angle(self, p1, p2, p3):
        # Square of lengths be a2, b2, c2
        a2 = self.length_square(p2, p3)
        b2 = self.length_square(p1, p3)
        c2 = self.length_square(p1, p2)

        # length of sides be a, b, c
        a = math.sqrt(a2)
        b = math.sqrt(b2)
        c = math.sqrt(c2)

        # From Cosine law
        if 2 * a *c != 0 :
            betta = math.acos((a2 + c2 - b2) /(2 * a * c))

            # Converting to degree
            betta = betta * 180 / math.pi

            return betta
        return -1


def main():
    A = (4, 3)
    B = (-4, 3)
    C = (-4, -3)
    angle = AngleCalculator()
    print(angle.get_angle(A, B, C))

if __name__ == "__main__":
    main()
