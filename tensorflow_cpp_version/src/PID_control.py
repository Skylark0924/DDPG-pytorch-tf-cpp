
from config import *


class ControlAlgorithm:
    def __init__(self):
        self.last_da = 0

    def choose_action(self, s):
        angle, target_angle = s[Q_LEN-1], s[2*Q_LEN - 1]
        da = target_angle - angle

        # P = 0.00001
        # D = 0.01

        # P = 0.00001
        # D = 0.1

        # P = 0.001
        # D = 0.1
        # P = 0.01
        # D = 1

        P = 0.05
        D = 0.5
        a = P * da + D * (da - self.last_da)

        self.last_da = da

        return a


