import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from label_antennas_field.objects_antennas_field import ObjectsAntennasField


class DrawingAntennasField:
    # Отступы от границы элемента
    padding_x = 40
    padding_y = 20
    # Кисти
    pen_grid = QtGui.QPen(Qt.black, 2)
    pen_text = QtGui.QPen(Qt.red, 1)
    # Шрифты
    font_text = QtGui.QFont("Times", 12)

    # Рисование сетки в pixmap
    # cells_width, cells_height - количество ячеек вдоль оси. Должны быть четными!!!
    @staticmethod
    def drawing_field(draw: ObjectsAntennasField):
        # Выбираем кисть
        draw.painter.setPen(DrawingAntennasField.pen_grid)  # Устанавливаем цвети размер

        # Считаем расстояние между линиями сетки в пикселях
        step_width = (draw.pixmap.width() - DrawingAntennasField.padding_x * 2) / draw.cells_width
        step_height = (draw.pixmap.height() - DrawingAntennasField.padding_y * 2) / draw.cells_height

        # Границы области отрисовки
        # По x - ширине width
        left_border = DrawingAntennasField.padding_x
        right_border = int(draw.pixmap.width() - DrawingAntennasField.padding_x)
        # По y - ширине height
        top_border = DrawingAntennasField.padding_y
        bottom_border = int(draw.pixmap.height() - DrawingAntennasField.padding_y)

        # Для вертикальных линий - координаты по x
        coordinates_x = np.arange((draw.cells_width + 1), dtype="float16")
        coordinates_x = (DrawingAntennasField.padding_x + coordinates_x * step_width).astype("uint16")
        # Для горизонтальных линий - координаты по x
        coordinates_y = np.arange((draw.cells_height + 1), dtype="float16")
        coordinates_y = (DrawingAntennasField.padding_y + coordinates_y * step_height).astype("uint16")

        # Отрисовка линий
        # Вертикальные - смещены по x
        for x_i in coordinates_x:
            draw.painter.drawLine(x_i, top_border, x_i, bottom_border)
        # Горизонтальные - смещены по y
        for y_i in coordinates_y:
            draw.painter.drawLine(left_border, y_i, right_border, y_i)

        return coordinates_x, coordinates_y

    # Подпись делений осей сетки в pixmap
    # cells_width, cells_height - количество ячеек вдоль оси. Должны быть четными!!!
    @staticmethod
    def drawing_axis_labels(
            draw: ObjectsAntennasField,
            coordinates_grids_x, coordinates_grids_y
    ):
        # Количество делений в одном направлении
        calibration_x = draw.cells_width // 2
        calibration_y = draw.cells_height // 2

        # Цена деления
        step_radius_x = draw.maximum_radius_value_x / calibration_x
        step_radius_y = draw.maximum_radius_value_y / calibration_y

        # Значения делений для координаты
        # По оси x
        val_calibration_x = np.arange(-calibration_x, calibration_x + 1, dtype="float16")
        val_calibration_x = val_calibration_x * step_radius_x
        # По оси y
        val_calibration_y = np.arange(calibration_y, -calibration_y - 1, -1, dtype="float16")
        val_calibration_y = val_calibration_y * step_radius_y

        # Оси располагаются по центру - считаем координаты центров
        center_x = draw.pixmap.width() // 2
        center_y = draw.pixmap.height() // 2

        # Ручка для написания теста и параметры текста
        draw.painter.setPen(DrawingAntennasField.pen_text)
        draw.painter.setFont(DrawingAntennasField.font_text)

        # Текст рисуется не посередине - исправим
        # Находим ширину текста и на это значение смещаем все подписи по x
        metrics = QtGui.QFontMetrics(DrawingAntennasField.font_text)
        text_width = metrics.boundingRect(f' {val_calibration_y[-1]: .1f}').width()
        coordinates_x = coordinates_grids_x - text_width // 2

        # Подписываем значения делений осй
        # Для оси y
        for line_i in range(draw.cells_height + 1):
            # Значение в 0 - пропускаем
            if line_i == draw.cells_height // 2:
                continue
            # Подпись значений
            draw.painter.drawText(center_x, coordinates_grids_y[line_i],
                                  f' {val_calibration_y[line_i]: .1f}')
        # Для оси x
        for column_i in range(draw.cells_width + 1):
            # Подпись значений
            draw.painter.drawText(coordinates_x[column_i], center_y,
                                  f' {val_calibration_x[column_i]: .1f}')


