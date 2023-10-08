import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from label_antennas_field.options_antennas_field import OptionsAntennasField


class DrawingAntennasField:
    # Отступы от границы элемента
    padding_x = 40
    padding_y = 20
    # Кисти
    pen_grid = QtGui.QPen(Qt.black, 2)
    pen_text = QtGui.QPen(Qt.red, 1)
    # Шрифты
    font_text = QtGui.QFont("Times", 12)
    # Заполнения
    brush = QtGui.QBrush(QtGui.QColor("#FFD141"), Qt.BrushStyle.Dense1Pattern)

    # Рисование сетки в pixmap
    # cells_width, cells_height - количество ячеек вдоль оси. Должны быть четными!!!
    @staticmethod
    def drawing_field(
            pixmap, painter,
            data_and_parameters: OptionsAntennasField):

        # Выбираем кисть
        painter.setPen(DrawingAntennasField.pen_grid)  # Устанавливаем цвети размер

        # Считаем расстояние между линиями сетки в пикселях
        step_width = (pixmap.width() - DrawingAntennasField.padding_x * 2) / data_and_parameters.cells_width
        step_height = (pixmap.height() - DrawingAntennasField.padding_y * 2) / data_and_parameters.cells_height

        # Границы области отрисовки
        # По x - ширине width
        left_border = DrawingAntennasField.padding_x
        right_border = int(pixmap.width() - DrawingAntennasField.padding_x)
        # По y - ширине height
        top_border = DrawingAntennasField.padding_y
        bottom_border = int(pixmap.height() - DrawingAntennasField.padding_y)

        # Для вертикальных линий - координаты по x
        coordinates_x = np.arange((data_and_parameters.cells_width + 1), dtype="float16")
        coordinates_x = (DrawingAntennasField.padding_x + coordinates_x * step_width).astype("uint16")
        # Для горизонтальных линий - координаты по x
        coordinates_y = np.arange((data_and_parameters.cells_height + 1), dtype="float16")
        coordinates_y = (DrawingAntennasField.padding_y + coordinates_y * step_height).astype("uint16")

        # Отрисовка линий
        # Вертикальные - смещены по x
        for x_i in coordinates_x:
            painter.drawLine(x_i, top_border, x_i, bottom_border)
        # Горизонтальные - смещены по y
        for y_i in coordinates_y:
            painter.drawLine(left_border, y_i, right_border, y_i)

        return coordinates_x, coordinates_y

    # Подпись делений осей сетки в pixmap
    # cells_width, cells_height - количество ячеек вдоль оси. Должны быть четными!!!
    @staticmethod
    def drawing_axis_labels(
            pixmap, painter,
            data_and_parameters: OptionsAntennasField,
            coordinates_grids_x, coordinates_grids_y
    ):
        # Количество делений в одном направлении
        calibration_x = data_and_parameters.cells_width // 2
        calibration_y = data_and_parameters.cells_height // 2

        # Цена деления
        step_radius_x = data_and_parameters.maximum_radius_value_x / calibration_x
        step_radius_y = data_and_parameters.maximum_radius_value_y / calibration_y

        # Значения делений для координаты
        # По оси x
        val_calibration_x = np.arange(-calibration_x, calibration_x + 1, dtype="float16")
        val_calibration_x = val_calibration_x * step_radius_x
        # По оси y
        val_calibration_y = np.arange(calibration_y, -calibration_y - 1, -1, dtype="float16")
        val_calibration_y = val_calibration_y * step_radius_y

        # Оси располагаются по центру - считаем координаты центров
        center_x = pixmap.width() // 2
        center_y = pixmap.height() // 2

        # Ручка для написания теста и параметры текста
        painter.setPen(DrawingAntennasField.pen_text)
        painter.setFont(DrawingAntennasField.font_text)

        # Текст рисуется не посередине - исправим
        # Находим ширину текста и на это значение смещаем все подписи по x
        metrics = QtGui.QFontMetrics(DrawingAntennasField.font_text)
        text_width = metrics.boundingRect(f' {val_calibration_y[-1]: .1f}').width()
        text_shift = text_width // 2

        coordinates_x = coordinates_grids_x - text_shift
        center_x = center_x - text_shift

        # Подписываем значения делений осй
        # Для оси y
        for line_i in range(data_and_parameters.cells_height + 1):
            # Значение в 0 - пропускаем
            if line_i == data_and_parameters.cells_height // 2:
                continue
            # Подпись значений
            painter.drawText(center_x, coordinates_grids_y[line_i],
                             f' {val_calibration_y[line_i]: .1f}')
        # Для оси x
        for column_i in range(data_and_parameters.cells_width + 1):
            # Подпись значений
            painter.drawText(coordinates_x[column_i], center_y,
                             f' {val_calibration_x[column_i]: .1f}')

    # Рисуем по таблице данных антенны
    @staticmethod
    def drawing_antennas(
            painter,
            data_and_parameters: OptionsAntennasField,
            coordinates_grids_x, coordinates_grids_y
    ):
        # Закрашиваем нужные данные
        painter.setBrush(DrawingAntennasField.brush)
        painter.setPen(DrawingAntennasField.pen_grid)

        cell_width = coordinates_grids_x[1] - coordinates_grids_x[0]
        cell_height = coordinates_grids_y[1] - coordinates_grids_y[0]

        for j in range(data_and_parameters.cells_height):
            for i in range(data_and_parameters.cells_width):
                if data_and_parameters.field[j][i]:
                    painter.drawRect(QtCore.QRect(coordinates_grids_x[i], coordinates_grids_y[j],
                                                  cell_width, cell_height))
