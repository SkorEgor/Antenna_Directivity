from gui import Ui_Dialog
from label_antennas_field.label_antennas_field import LabelAntennasField
from PyQt5.QtCore import Qt

# КЛАСС АЛГОРИТМА ПРИЛОЖЕНИЯ
class GuiProgram(Ui_Dialog):

    def __init__(self, dialog):
        # ПОЛЯ КЛАССА


        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Создаем окно
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)  # Устанавливаем пользовательский интерфейс

        self.label_field_antennas = LabelAntennasField(
            cells_width=10, cells_height=10,
            maximum_radius_value_x=1, maximum_radius_value_y=1
        )
        self.plotLayout.addWidget(self.label_field_antennas)

