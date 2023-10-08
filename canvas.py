import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen

import numpy as np



class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)

        pixmap.fill(Qt.white)

        pixmap.scaled(self.width(), self.height())
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

    def resizeEvent(self, event):
        self.my_paint()
        # pixmap = self.pixmap()
        #
        # pixmap = pixmap.scaled(self.width(), self.height())
        #
        # self.setPixmap(pixmap)
        # print(self.width(), self.height())

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    # def resizeEvent(self, event):
    #     pixmap = self.pixmap()
    #
    #     pixmap = pixmap.scaled(self.width(), self.height())
    #
    #     self.setPixmap(pixmap)
    #     print(self.width(), self.height())

    # Рисование сетки
    def my_paint(self):
        # (0) Получаем объекты для рисования
        #canvas = self.pixmap()  # Пиксельная карта на которой рисуем
        canvas = QtGui.QPixmap(self.width(), self.height())
        canvas.fill(Qt.white)
        painter = QtGui.QPainter(canvas)  # Кисть рисования

        # Выбираем параметры кисти
        # painter.setPen(QPen(Qt.green, 8, Qt.DashLine))

        # Находим размеры
        padding_x = 40
        padding_y = 20

        cells_width = 4
        cells_height = 4

        step_width = (canvas.width() - padding_x * 2) / cells_width
        step_height = (canvas.height() - padding_y * 2) / cells_height

        left_border = padding_x
        right_border = int(canvas.width() - padding_x)

        top_border = padding_y
        bottom_border = int(canvas.height() - padding_y)

        coordinates_y = np.arange((cells_height + 1), dtype="float16")
        coordinates_y = (padding_y + coordinates_y * step_height).astype("uint16")

        coordinates_x = np.arange((cells_width + 1), dtype="float16")
        coordinates_x = (padding_x + coordinates_x * step_width).astype("uint16")

        for y_i in coordinates_y:
            painter.drawLine(left_border, y_i, right_border, y_i)

        for x_i in coordinates_x:
            painter.drawLine(x_i, top_border, x_i, bottom_border)

        radius_x = 40
        radius_y = 80

        calibration_x = cells_width//2
        calibration_y = cells_height//2

        step_radius_x = radius_x / calibration_x
        step_radius_y = radius_y / calibration_y

        val_calibration_x = np.arange(-calibration_x, calibration_x +1, dtype="float16")
        val_calibration_x = val_calibration_x * step_radius_x

        val_calibration_y = np.arange(calibration_y, -calibration_y -1, -1,  dtype="float16")
        val_calibration_y = val_calibration_y * step_radius_y

        center_x = canvas.width()//2
        center_y = canvas.height() // 2

        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('green'))
        painter.setPen(pen)

        font = QtGui.QFont()
        font.setFamily('Times')
        font.setPointSize(12)
        painter.setFont(font)

        for line_i in range(cells_height + 1):
            if line_i==cells_height//2:
                continue
            painter.drawText(center_x, coordinates_y[line_i],
                             f' {val_calibration_y[line_i]: .1f}')

        metrics = QtGui.QFontMetrics(font)
        print(metrics.boundingRect(f' {val_calibration_y[-1]: .1f}').width())
        coordinates_x = coordinates_x - metrics.boundingRect(f' {val_calibration_y[-1]: .1f}').width()//2
        for column_i in range(cells_width + 1):
            painter.drawText(coordinates_x[column_i], center_y,
                             f' {val_calibration_x[column_i]: .1f}')

        painter.end()
        self.setPixmap(canvas)

        painter = QPainter(self)
