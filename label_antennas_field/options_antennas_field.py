import numpy as np


class OptionsAntennasField:
    def __init__(self):
        # Параметры поля
        self.cells_width = 8
        self.cells_height = 4
        self.maximum_radius_value_x = 40
        self.maximum_radius_value_y = 80
        self.field = np.full((self.cells_height, self.cells_width), False)
