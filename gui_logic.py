from gui import Ui_Dialog
from canvas import Canvas
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

# КЛАСС АЛГОРИТМА ПРИЛОЖЕНИЯ
class GuiProgram(Ui_Dialog):

    def __init__(self, dialog):
        # ПОЛЯ КЛАССА


        # ДЕЙСТВИЯ ПРИ ВКЛЮЧЕНИИ
        # Создаем окно
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)  # Устанавливаем пользовательский интерфейс

        self.canvas = Canvas()
        self.plotLayout.addWidget(self.canvas)


        self.last_x, self.last_y = None, None

        self.pushButton.clicked.connect(self.canvas.my_paint)
