from PySide6 import QtWidgets
from window_b import Ui_Dialog


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.__initUi()

    def __initUi(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()