import numpy as np


class ObjectsAntennasField:
    def __init__(self, pixmap, painter):
        # Параметры поля
        self.cells_width = 4
        self.cells_height = 4
        self.maximum_radius_value_x = 40
        self.maximum_radius_value_y = 80

        # Объекты для рисования
        self.pixmap = pixmap
        self.painter = painter
