from PySide6 import QtWidgets
#from window_b import Ui_Dialog
from Practice_1.window_c.window_c import Ui_Parametry

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.__initUi()

    def __initUi(self):
        self.ui = Ui_Parametry()
        self.ui.setupUi(self)


        # self.setWindowTitle("Тестовое окно")
        # self.resize(400, 200)
        # self.move(50, 50)
        #
        # self.lineEditLogin = QtWidgets.QLineEdit()
        # self.lineEditLogin.setPlaceholderText("Введите Ваше имя")
        #
        # self.lineEditPassword = QtWidgets.QLineEdit()
        # self.lineEditPassword.setPlaceholderText("Введите Ваш пароль")
        # self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        #
        # self.pbOk = QtWidgets.QPushButton("Ок")
        # self.pbCancel = QtWidgets.QPushButton()
        # self.pbCancel.setText("Cancel")
        #
        # spacer = QtWidgets.QSpacerItem(
        #     10, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding
        # )
        #
        # l_buttons = QtWidgets.QHBoxLayout()
        # l_buttons.addWidget(self.pbOk)
        # l_buttons.addWidget(self.pbCancel)
        #
        # l_main = QtWidgets.QVBoxLayout()
        # l_main.addWidget(self.lineEditLogin)
        # l_main.addWidget(self.lineEditPassword)
        # l_main.addSpacerItem(spacer)
        # l_main.addLayout(l_buttons)
        #
        # self.setLayout(l_main)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()