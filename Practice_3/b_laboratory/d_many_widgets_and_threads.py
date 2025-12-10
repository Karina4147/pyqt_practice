"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets
from b_systeminfo_widget import Window as Window1
from c_weatherapi_widget import Window as Window2


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Объединенное окно")
        self.setGeometry(100, 100, 600, 400)

        self.widget1_instance = Window1()
        self.widget2_instance = Window2()

        self.main_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.widget1_instance)
        self.main_layout.addWidget(self.widget2_instance)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()