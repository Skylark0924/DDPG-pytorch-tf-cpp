
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import math

from PyQt5.QtCore import Qt, QSize, QPoint, QTimer
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QDialogButtonBox,QGraphicsView,QGraphicsScene)
from PyQt5.QtCore import QMutex, QThread, QWaitCondition


MTX = QMutex()
X_LEN = 3000
Y = np.zeros(X_LEN)
Y_UP = np.zeros(X_LEN)
Y_DOWN = np.zeros(X_LEN)
Y_ = np.zeros(X_LEN)


def set_UI_DATA(target, act):
    global Y, Y_UP, Y_DOWN, Y_
    MTX.lock()

    Y = np.roll(Y, -1)
    Y[-1] = target

    Y_ = np.roll(Y_, -1)
    Y_[-1] = act

    MTX.unlock()


class Panel(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.init_fig()
        self.canvas = FigureCanvas(self.fig)

        self.graphicscene = QGraphicsScene()
        self.graphicscene.addWidget(self.canvas)
        self.setScene(self.graphicscene)
        self.setFixedSize(950, 650)

        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_timer)
        self.timer.setInterval(50)
        self.timer.start()

    def handle_timer(self):
        self.line_target.set_ydata(Y)
        self.line_act.set_ydata(Y_)
        self.fig.canvas.draw()

    def init_fig(self):
        self.fig = Figure(figsize=(9, 6), dpi=100)
        axes = self.fig.add_subplot(111)

        axes.set_ylim(-10, 100)
        axes.set_xlim(0, X_LEN)

        self.x = np.arange(0, X_LEN)
        self.y = np.zeros(X_LEN)
        self.line_target, = axes.plot(self.x, self.y, color='C0')

        self.x_ = np.arange(0, X_LEN)
        self.y_ = np.zeros(X_LEN)
        self.line_act, = axes.plot(self.x_, self.y_, color='C3')

        # self.fig.tight_layout()

