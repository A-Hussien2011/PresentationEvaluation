import math


class AngleCalculator:
    def __init__(self, point1, point2, point3):
        self.p1 = point1
        self.p2 = point2
        self.p3 = point3

    # returns square of distance b/w two points
    def length_square(self,X, Y):
        x_diff = X[0] - Y[0]
        y_diff = X[1] - Y[1]
        return x_diff * x_diff + y_diff * y_diff

    def get_angle(self):
        # Square of lengths be a2, b2, c2
        a2 = self.length_square(self.p2, self.p3)
        b2 = self.length_square(self.p1, self.p3)
        c2 = self.length_square(self.p1, self.p2)

        # length of sides be a, b, c
        a = math.sqrt(a2)
        b = math.sqrt(b2)
        c = math.sqrt(c2)

        # From Cosine law
        betta = math.acos((a2 + c2 - b2) /(2 * a * c))

        # Converting to degree
        betta = betta * 180 / math.pi

        return betta


def main():
    A = (0, 0)
    B = (0, 1)
    C = (1, 0)
    angle = AngleCalculator(A, B, C)
    print(angle.get_angle())


if __name__ == "__main__":
    main()
