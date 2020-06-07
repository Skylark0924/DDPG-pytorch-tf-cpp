
import numpy as np
import math

A = 40.
Y0 = 50.


class TargetData:
    def __init__(self, target_type='sin'):
        if target_type == 'sin':
            self.data = [Y0 for _ in range(100)] + \
                        [Y0 + A * math.sin(i / 200 * 2 * math.pi) for i in range(200)] + \
                        [Y0 for _ in range(100)] + [0. for _ in range(100)]

        elif target_type == 'jump':
            self.data = [Y0 for _ in range(500)]

        elif target_type == 'slop':
            self.data = [2*Y0 * i / 500 for i in range(500)]

    def get_time_all(self):
        return len(self.data) / 2 - 5

    @staticmethod
    def get_target_v_by_t_internal(t, data):
        i_l = int(t // 0.5)
        rate = (t % 0.5) / 0.5
        return (1 - rate) * data[i_l] + rate * data[i_l+1]

    def get_target_v_by_t(self, t):
        return self.get_target_v_by_t_internal(t, self.data)

    def get_target_a_by_t(self, t):
        data = self.data
        i_l = int(t // 0.5)
        rate = (t % 0.5) / 0.5
        if rate < 0.5:
            rate_a = rate + 0.5
            target_a = ((1 - rate_a) * (data[i_l] - data[i_l-1]) / 0.5
                        + rate_a * (data[i_l+1] - data[i_l]) / 0.5) / 3.6
        else:
            rate_a = rate - 0.5
            target_a = ((1 - rate_a) * (data[i_l+1] - data[i_l]) / 0.5
                        + rate_a * (data[i_l+2] - data[i_l+1]) / 0.5) / 3.6
        return target_a
