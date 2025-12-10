"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets

from a_threads import SystemInfo

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.init_ui()
        self.init_thread()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        self.delay_input = QtWidgets.QLineEdit(self)
        self.delay_input.setText("1.0")
        self.delay_input.editingFinished.connect(self.update_delay)
        form_layout.addRow(QtWidgets.QLabel("Задержка (сек):"), self.delay_input)

        self.cpu_label = QtWidgets.QLabel("0.0 %", self)
        form_layout.addRow(QtWidgets.QLabel("Загрузка CPU:"), self.cpu_label)

        self.ram_label = QtWidgets.QLabel("0.0 %", self)
        form_layout.addRow(QtWidgets.QLabel("Загрузка RAM:"), self.ram_label)

        layout.addLayout(form_layout)
        self.setLayout(layout)

    def init_thread(self):
        self.system_thread = SystemInfo()
        self.system_thread.systemInfoReceived.connect(self.update_labels)
        self.system_thread.start()

    def update_labels(self, cpu_usage, ram_usage):
        self.cpu_label.setText(f"{cpu_usage:.1f} %")
        self.ram_label.setText(f"{ram_usage:.1f} %")

    def update_delay(self):
        try:
            new_delay = float(self.delay_input.text())
            if new_delay > 0:
                self.system_thread.delay(new_delay)
        except ValueError:
            self.delay_input.setText(str(self.system_thread.delay))

if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()