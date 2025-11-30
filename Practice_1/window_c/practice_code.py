from PySide6 import QtWidgets
from Practice_1.window_c.window_c import Ui_Parametry

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.__initUi()

    def __initUi(self):
        self.ui = Ui_Parametry()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()