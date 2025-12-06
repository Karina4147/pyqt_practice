"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущий основной монитор
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtCore, QtGui
from c_signals_events_form import Ui_Form
import datetime


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()

    def __initUi(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButtonLT.clicked.connect(lambda: self.move(0, 0))
        self.ui.pushButtonRT.clicked.connect(self.onPushButtonRT)
        self.ui.pushButtonRB.clicked.connect(self.onPushButtonRB)
        self.ui.pushButtonLB.clicked.connect(self.onPushButtonLB)
        self.ui.pushButtonCenter.clicked.connect(self.onPushButtonCenter)
        self.ui.pushButtonMoveCoords.clicked.connect(lambda: self.move(self.ui.spinBoxX.value(), self.ui.spinBoxY.value()))
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetData)

    def onPushButtonCenter(self):
        x = (self.screen_geometry.width() - self.width()) // 2
        y = (self.screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def onPushButtonRT(self):
        x = (self.screen_geometry.right() - self.width())
        self.move(x, 0)

    def onPushButtonRB(self):
        x = (self.screen_geometry.right() - self.width())
        y = (self.screen_geometry.bottom() - self.height())
        self.move(x, y)

    def onPushButtonLB(self):
        x = self.screen_geometry.left()
        y = (self.screen_geometry.bottom() - self.height())
        self.move(x, y)

        print(QtGui.QGuiApplication.screens())

    def moveEvent(self, event, /):
        print(event.pos())
        print(event.oldPos())
        super().moveEvent(event)

    def onPushButtonGetData(self):
        screens = QtWidgets.QApplication.screens()
        primary_screen = QtWidgets.QApplication.primaryScreen()
        geom = primary_screen.geometry()
        window_pos = self.pos()
        window_rect = self.frameGeometry()
        center_point = window_rect.center()
        min_size = self.minimumSize()

        self.ui.plainTextEdit.setPlainText(f"Время: {datetime.datetime.now().strftime('%H:%M:%S')}")
        self.ui.plainTextEdit.appendPlainText(f"Кол-во экранов: {len(screens)}")
        self.ui.plainTextEdit.appendPlainText(f"Текущий основной монитор: {primary_screen.name()}")
        self.ui.plainTextEdit.appendPlainText(f"Разрешение экрана: {geom.width()}x{geom.height()}")
        self.ui.plainTextEdit.appendPlainText(f"Экран на котором окно находится: {window.screen().name()}")
        self.ui.plainTextEdit.appendPlainText(f"Размеры окна (W x H): {window.size().toTuple()}")
        self.ui.plainTextEdit.appendPlainText(f"Минимальный размер окна: {min_size.width()} x {min_size.height()}")
        self.ui.plainTextEdit.appendPlainText(f"Текущее положение (координаты) окна: {window_pos.x()}, {window_pos.y()}")
        self.ui.plainTextEdit.appendPlainText(f"Координаты центра приложения: {center_point.x()}, {center_point.y()}")
        self.ui.plainTextEdit.appendPlainText(f"Свернуто: {self.isMinimized()}")
        self.ui.plainTextEdit.appendPlainText(f"Развёрнуто: {self.isMaximized()}")
        self.ui.plainTextEdit.appendPlainText(f"Активно: {self.isActiveWindow()}")
        self.ui.plainTextEdit.appendPlainText(f"Отображено: {self.isVisible()}")

    def _now(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def track_window_state(self):
        """Отслеживание состояния окна."""
        if self.isMinimized():
            state = "Свернуто"
        elif self.isMaximized():
            state = "Развёрнуто"
        elif self.isActiveWindow():
            state = "Активно"
        elif self.isVisible():
            state = "Отображено"
        else:
            state = "Неизвестно/Скрыто"

        if not hasattr(self, '_last_state') or self._last_state != state:
            self.log_message(f"Состояние окна: {state}")
            self._last_state = state


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
