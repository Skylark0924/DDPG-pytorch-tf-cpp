
import sys
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

import numpy as np

from throttle_simulation import ThrottleSimulation
from PID_control import ControlAlgorithm
from panel import Panel
from RL_DDPG import DDPG, MEMORY_CAPACITY
from config import *


RUNNING_TYPE = 'train'  # 'train', 'test'
TARGET_TYPE = 'sin'  # 'sin', 'jump', 'slop'

TRAIN_TIMES = 80  # 8， 150
ACTION_BOUND = 1
VAR_INIT = 0.02  # 1
VAR_MIN = 0.000001
ATTENUATION = 0.99998


class Backend(QThread):

    def train(self):
        throttle = ThrottleSimulation(target_type=TARGET_TYPE)
        RL = DDPG(1, 2* Q_LEN, [ACTION_BOUND])
        RL.restore_net()

        var = VAR_INIT
        for i in range(TRAIN_TIMES):
            s = throttle.reset(0.1)
            while True:
                a = RL.choose_action(s)
                a = np.clip(np.random.normal(a, var), -ACTION_BOUND, ACTION_BOUND)
                # a = np.clip(a, -ACTION_BOUND, ACTION_BOUND)

                s_, r, done = throttle.step(a[0])
                if done:
                    break
                RL.store_transition(s, a, r, s_)

                if RL.pointer > 500:
                    var *= ATTENUATION
                    var = max(var, VAR_MIN)
                    RL.learn()

                s = s_
                # self.msleep(2)

            print('episode: {}  VAR:{}'.format(i, var))
            RL.save()

    def test(self):
        throttle = ThrottleSimulation(target_type=TARGET_TYPE)
        control = ControlAlgorithm()

        s = throttle.reset(0.1)
        while True:
            a = control.choose_action(s)
            s, r, done = throttle.step(a)
            if done:
                break
            # self.msleep(2)

        print('done.')

    def run(self):
        if RUNNING_TYPE == 'train':
            self.train()
        elif RUNNING_TYPE == 'test':
            self.test()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    back = Backend()
    back.start()

    panel = Panel()
    panel.show()

    sys.exit(app.exec_())


