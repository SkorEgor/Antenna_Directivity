from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from label_antennas_field.options_antennas_field import OptionsAntennasField
from label_antennas_field.drawing_antennas_field import DrawingAntennasField

import numpy as np


class LabelAntennasField(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()

        self.data_and_parameters = OptionsAntennasField()

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

        # Координаты сетки
        self.coordinates_grids_x = np.array([])
        self.coordinates_grids_y = np.array([])

    def resizeEvent(self, event):
        self.my_paint()

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

    # Обработка нажатия клавиши - Отмечаем ячейку в которую попали
    def mousePressEvent(self, event):
        # (1) Получаем координаты клика
        clicking_x = event.x()
        clicking_y = event.y()

        # (3) Проверка на клик в область таблицы - иначе сброс
        # По x
        if not (self.coordinates_grids_x[0] <= clicking_x <= self.coordinates_grids_x[-1]):
            return
        # По y
        if not (self.coordinates_grids_y[0] <= clicking_y <= self.coordinates_grids_y[-1]):
            return

        # (4) Находим индексы ячеек
        # По x
        index_x = self.coordinates_grids_x[self.coordinates_grids_x < clicking_x].size - 1
        # По y
        index_y = self.coordinates_grids_y[self.coordinates_grids_y < clicking_y].size - 1

        # В найденной ячейке меняем значение на противоположное
        self.data_and_parameters.field[index_y][index_x] = not self.data_and_parameters.field[index_y][index_x]
        self.my_paint()     # Обновляем рисунок

    # Рисование сетки
    def my_paint(self):
        # (0) Получаем объекты для рисования
        # Пиксельная карта на которой рисуем
        # canvas = self.pixmap()
        pixmap = QtGui.QPixmap(self.width(), self.height())
        pixmap.fill(Qt.white)
        # Кисть рисования на холсте - pixmap
        painter = QtGui.QPainter(pixmap)

        # (1) Рисуем сетку
        self.coordinates_grids_x, self.coordinates_grids_y = \
            DrawingAntennasField.drawing_field(pixmap, painter,
                                               self.data_and_parameters)

        # (2) Закрашиваем нужные данные
        DrawingAntennasField.drawing_antennas(
            painter,
            self.data_and_parameters,
            self.coordinates_grids_x, self.coordinates_grids_y)

        # (3) Подписываем оси
        DrawingAntennasField.drawing_axis_labels(
            pixmap, painter,
            self.data_and_parameters,
            self.coordinates_grids_x, self.coordinates_grids_y)

        painter.end()
        self.setPixmap(pixmap)
