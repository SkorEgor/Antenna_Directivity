from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from label_antennas_field.options_antennas_field import OptionsAntennasField
from label_antennas_field.drawing_antennas_field import DrawingAntennasField

import numpy as np


class LabelAntennasField(QtWidgets.QLabel):

    def __init__(self,
                 cells_width, cells_height,
                 maximum_radius_value_x=1, maximum_radius_value_y=1):
        super().__init__()
        # Параметры поля с антеннами и данные о нахождении антенн
        self.data_and_parameters = OptionsAntennasField(
            cells_width, cells_height,
            maximum_radius_value_x, maximum_radius_value_y)

        # Координаты сетки
        self.coordinates_grids_x = np.array([])
        self.coordinates_grids_y = np.array([])

    # При изменении размера элемента - перерисовка
    def resizeEvent(self, event):
        self.my_paint()

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
