from PySide6 import QtWidgets, QtCore, QtGui
from function import SystemInfo

class MetricsTableModel(QtGui.QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Ресурс", "Значение"])
        self.setRowCount(4)

        self.setItem(0, 0, QtGui.QStandardItem("CPU (%)"))
        self.setItem(1, 0, QtGui.QStandardItem("RAM (GB)"))
        self.setItem(2, 0, QtGui.QStandardItem("Диск (GB)"))
        self.setItem(3, 0, QtGui.QStandardItem("Время обновления"))

    def update_metrics(self, metrics):
        self.setItem(0, 1, QtGui.QStandardItem(metrics['CPU']))
        self.setItem(1, 1, QtGui.QStandardItem(metrics['RAM']))
        self.setItem(2, 1, QtGui.QStandardItem(metrics['Disk']))
        self.setItem(3, 1, QtGui.QStandardItem(metrics['Last Update']))

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мониторинг Системы")
        self.setGeometry(100, 100, 500, 300)

        self.worker = None
        self.worker_thread = None
        self.is_monitoring = False

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.table_model = MetricsTableModel()
        self.table_view = QtWidgets.QTableView()
        self.table_view.setModel(self.table_model)

        self.table_view.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)
        main_layout.addWidget(self.table_view)

        control_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(control_layout)

        self.start_button = QtWidgets.QPushButton("Старт")
        self.stop_button = QtWidgets.QPushButton("Стоп")
        self.stop_button.setEnabled(False)

        self.interval_label = QtWidgets.QLabel("Интервал (мс):")
        self.interval_spinbox = QtWidgets.QSpinBox()
        self.interval_spinbox.setRange(100, 5000)
        self.interval_spinbox.setValue(1000)

        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addStretch()
        control_layout.addWidget(self.interval_label)
        control_layout.addWidget(self.interval_spinbox)

    def _connect_signals(self):
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button.clicked.connect(self.stop_monitoring)

        self.interval_spinbox.valueChanged.connect(self.change_interval)

    def start_monitoring(self):
        """Запускает поток мониторинга."""
        if self.is_monitoring:
            return

        self.worker_thread = QtCore.QThread()
        self.worker = SystemInfo()

        self.worker.moveToThread(self.worker_thread)

        self.worker.metrics_updated.connect(self.update_ui)
        self.worker.stopped.connect(self.on_worker_stopped)
        self.worker.error.connect(self.display_error)

        self.worker_thread.started.connect(self.worker.run)

        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker.deleteLater()

        self.worker.set_interval(self.interval_spinbox.value())

        self.worker_thread.start()
        self.is_monitoring = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.interval_spinbox.setEnabled(False)

    def stop_monitoring(self):
        """Останавливает поток мониторинга."""
        if not self.is_monitoring:
            return

        if self.worker:
            self.worker.stop()

    def on_worker_stopped(self):
        """Слот, вызываемый после фактической остановки цикла worker'а."""
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()

        self.is_monitoring = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.interval_spinbox.setEnabled(True)
        self.worker = None
        self.worker_thread = None

    def update_ui(self, metrics):
        """Слот, обновляющий UI новыми данными (вызывается из главного потока)."""
        self.table_model.update_metrics(metrics)

    def change_interval(self, value):
        """Слот для изменения интервала опроса."""

        if self.worker and self.is_monitoring:
            self.worker.set_interval(value)


    def display_error(self, message):
        """Слот для отображения ошибок."""
        print(f"ERROR: {message}")
        self.stop_monitoring()

    def closeEvent(self, event):
        """Корректное завершение при закрытии окна приложения."""
        self.stop_monitoring()

        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.wait(2000)
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()