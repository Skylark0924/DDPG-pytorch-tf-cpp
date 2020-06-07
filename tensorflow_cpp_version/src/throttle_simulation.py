
from collections import deque
import numpy as np
import math

from target_data import TargetData
from panel import set_UI_DATA
from config import *

INSTRUCTION_DELAY = 3  # 7, 4
M_DELAY = 2  # 4, 2
MEASURE_DELAY = 1  # 3, 1

GAP = 0.


class ThrottleSimulation:
    def __init__(self, target_type='sin'):
        self.target_data = TargetData(target_type=target_type)
        self.time_all = self.target_data.get_time_all()

    def reset(self, dt):
        self.dt = dt

        self.angle = 0.
        self.angle_queue = np.zeros(Q_LEN)
        self.angle_gap = GAP
        self.v = 0.
        self.load = 0.

        self.target_angle = 0.
        self.target_angle_queue = np.zeros(Q_LEN)

        self.time = 0
        self.done = False

        return self._get_obs()

    def step(self, a):

        def update_actual_v_a(a):
            max_a = 0.3  # 0.3  50
            a = min(a, max_a)
            a = max(a, -max_a)

            if self.target_angle - self.angle > 20:
                a = max(0, a)
            if self.target_angle - self.angle < -20:
                a = min(0, a)

            self.load = 0.05 * math.sin(self.time / 20 * 2 * math.pi)
            a = a - self.load

            self.v += 1*a
            # self.angle += 1*self.v

            if self.v > GAP - self.angle_gap:
                self.angle_gap = GAP
                self.angle += self.v - (GAP - self.angle_gap)
            elif self.v < -GAP - self.angle_gap:
                self.angle_gap = -GAP
                self.angle += self.v - (-GAP - self.angle_gap)
            else:
                self.angle_gap += self.v
            self.angle_queue = np.roll(self.angle_queue, -1)
            self.angle_queue[-1] = self.angle

        update_actual_v_a(a)
        set_UI_DATA(self.target_angle, self.angle)

        def get_reward():
            delta_angle = abs(self.angle-self.target_angle)
            return -1 * delta_angle

        reward = get_reward()

        self.update_target_a_time()

        return self._get_obs(), reward, self.done

    def update_target_a_time(self):
        self.time += self.dt
        if self.time >= self.time_all:
            self.time = self.time_all
            self.done = True

        self.target_angle = self.target_data.get_target_v_by_t(self.time)
        self.target_angle_queue = np.roll(self.target_angle_queue, -1)
        self.target_angle_queue[-1] = self.target_angle

    def _get_obs(self):
        # return np.array([self.angle, self.target_data.get_target_v_by_t(self.time)])
        # return np.array(np.concatenate((self.angle_queue, self.target_angle_queue)))

        # return np.array([self.target_angle, self.angle])
        return np.array([i for i in self.angle_queue]
                        + [i for i in self.target_angle_queue]
                        + [self.load])




