"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

from PySide6 import QtWidgets
from a_threads import WeatherHandler

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.__initUi()
        self.__initSignals()

    def __initUi(self):
        self.lat_input = QtWidgets.QLineEdit(self)
        self.lat_input.setPlaceholderText('Широта')
        self.lon_input = QtWidgets.QLineEdit(self)
        self.lon_input.setPlaceholderText('Долгота')

        self.delay_input = QtWidgets.QLineEdit(self)
        self.delay_input.setPlaceholderText('Задержка (секунды)')
        self.delay_input.setText("5")

        self.weather_output = QtWidgets.QTextEdit(self)
        self.weather_output.setReadOnly(True)

        self.buttonStart = QtWidgets.QPushButton("Старт")
        self.buttonStart.setCheckable(True)

        layout = QtWidgets.QVBoxLayout()

        h_layout1 = QtWidgets.QHBoxLayout()
        h_layout1.addWidget(QtWidgets.QLabel("Координаты:"))
        h_layout1.addWidget(self.lat_input)
        h_layout1.addWidget(self.lon_input)
        layout.addLayout(h_layout1)

        h_layout2 = QtWidgets.QHBoxLayout()
        h_layout2.addWidget(QtWidgets.QLabel("Задержка:"))
        h_layout2.addWidget(self.delay_input)
        layout.addLayout(h_layout2)

        layout.addWidget(QtWidgets.QLabel("Информация о погоде:"))
        layout.addWidget(self.weather_output)
        layout.addWidget(self.buttonStart)

        self.setLayout(layout)

    def __initSignals(self):
        self.buttonStart.clicked.connect(self.__handleMainThread)

    def __handleMainThread(self, status):
        self.buttonStart.setText("Стоп" if status else "Старт")
        if not status:
            self.thread.stop()
        else:
            if self.lat_input.text() and self.lon_input.text():
                self.thread = WeatherHandler(lat=self.lat_input.text(), lon=self.lon_input.text())
                self.thread.started.connect(lambda:self.disable())
                self.thread.progress.connect(lambda data: self.appendWeatherInfo(data))
                self.thread.finished.connect(lambda: self.buttonStart.setChecked(False))
                self.thread.finished.connect(lambda: self.disable(status=True))
                self.thread.finished.connect(lambda: self.buttonStart.setText("Старт"))
                self.thread.start()

    def appendWeatherInfo(self, text):
        self.weather_output.insertPlainText(f"{text}")

    def disable(self, status=False):
        self.lon_input.setEnabled(status)
        self.lat_input.setEnabled(status)


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()