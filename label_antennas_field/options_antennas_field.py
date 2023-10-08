import numpy as np


class OptionsAntennasField:
    def __init__(self,
                 cells_width, cells_height,
                 maximum_radius_value_x, maximum_radius_value_y):
        # Параметры поля
        self.cells_width = cells_width
        self.cells_height = cells_height
        self.maximum_radius_value_x = maximum_radius_value_x
        self.maximum_radius_value_y = maximum_radius_value_y
        self.field = np.full((self.cells_height, self.cells_width), False)

    # Обновление параметров
    def new_parameters(self,
                       cells_width, cells_height,
                       maximum_radius_value_x, maximum_radius_value_y):
        # Параметры поля
        self.cells_width = cells_width
        self.cells_height = cells_height
        self.maximum_radius_value_x = maximum_radius_value_x
        self.maximum_radius_value_y = maximum_radius_value_y
        self.reset_field()

    # Обновление поля - зануленное
    def reset_field(self):
        self.field = np.full((self.cells_height, self.cells_width), False)
