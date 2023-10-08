from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from label_antennas_field.objects_antennas_field import ObjectsAntennasField
from label_antennas_field.drawing_antennas_field import DrawingAntennasField


class LabelAntennasField(QtWidgets.QLabel):

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
        DrawingAntennasField.drawing_field(objects_antennas_field)

        # (2) Подписываем оси
        DrawingAntennasField.drawing_axis_labels(objects_antennas_field)

        painter.end()
        self.setPixmap(pixmap)
