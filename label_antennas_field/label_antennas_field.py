from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt

from label_antennas_field.objects_antennas_field import ObjectsAntennasField
from label_antennas_field.drawing_antennas_field import DrawingAntennasField

import numpy as np
class LabelAntennasField(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(600, 300)

        pixmap.fill(Qt.white)

        pixmap.scaled(self.width(), self.height())
        self.setPixmap(pixmap)

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

    # Обработка нажатия клавиши
    def mousePressEvent(self, event):

        print(event.x(), event.y())
        # (1) Получаем координаты клика
        clicking_x = event.x()
        clicking_y = event.y()

        # (2) Отношение координат к координатам сетки
        # По x
        bool_x_min = self.coordinates_grids_x < clicking_x
        bool_x_max = self.coordinates_grids_x > clicking_x
        # По y
        bool_y_min = self.coordinates_grids_y < clicking_y
        bool_y_max = self.coordinates_grids_y > clicking_y


        # (3) Проверка на клик в область таблицы - иначе сброс
        # По x
        if np.all(bool_x_min) or np.all(bool_x_max):
            return
        # По y
        if np.all(bool_y_min) or np.all(bool_y_max):
            return

        # (4) Находим значение начала и конца ячейки
        # По x
        x_min = self.coordinates_grids_x[bool_x_min][-1]
        x_max = self.coordinates_grids_x[bool_x_max][0]
        # По y
        y_min = self.coordinates_grids_y[bool_y_min][-1]
        y_max = self.coordinates_grids_y[bool_y_max][0]

        print("x  ", x_min,x_max)
        print("y  ", y_min,y_max)

        pixmap = self.pixmap()
        painter = QtGui.QPainter(pixmap)

        painter.setPen(DrawingAntennasField.pen_grid)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor("#FFD141"))
        brush.setStyle(Qt.BrushStyle.Dense1Pattern)
        painter.setBrush(brush)

        painter.drawRect(QtCore.QRect(x_min, y_min,
                                  x_max-x_min, y_max-y_min))
        painter.end()
        self.setPixmap(pixmap)


    # Рисование сетки
    def my_paint(self):
        # (0) Получаем объекты для рисования
        # Пиксельная карта на которой рисуем
        # canvas = self.pixmap()
        pixmap = QtGui.QPixmap(self.width(), self.height())
        pixmap.fill(Qt.white)
        # Кисть рисования на холсте - pixmap
        painter = QtGui.QPainter(pixmap)

        objects_antennas_field = ObjectsAntennasField(pixmap=pixmap,
                                                      painter=painter)

        # (1) Рисуем сетку
        self.coordinates_grids_x, self.coordinates_grids_y =\
            DrawingAntennasField.drawing_field(objects_antennas_field)

        # (2) Подписываем оси
        DrawingAntennasField.drawing_axis_labels(objects_antennas_field,
                                                 self.coordinates_grids_x, self.coordinates_grids_y)

        painter.end()
        self.setPixmap(pixmap)
