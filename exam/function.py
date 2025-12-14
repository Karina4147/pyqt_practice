import time
from PySide6 import QtCore
import psutil
from datetime import datetime

class SystemInfo(QtCore.QObject):
    metrics_updated = QtCore.Signal(dict)
    stopped = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True
        self._interval = 1000

    def set_interval(self, ms):
        self._interval = ms

    def run(self):
        """Основной цикл сбора данных."""
        self._running = True
        while self._running:
            try:
                metrics = self.collect_metrics()
                self.metrics_updated.emit(metrics)
                time.sleep(self._interval / 1000.0)
            except Exception as e:
                self.error.emit(f"Ошибка сбора данных: {e}")
                break
        self.stopped.emit()

    def collect_metrics(self):
        """Собирает реальные данные с помощью psutil."""
        cpu_percent = psutil.cpu_percent(interval=None)  # Неблокирующий вызов

        ram = psutil.virtual_memory()
        ram_used = f"{ram.used / (1024 ** 3):.2f} GB"
        ram_avail = f"{ram.available / (1024 ** 3):.2f} GB"

        disk = psutil.disk_usage('/')
        disk_used = f"{disk.used / (1024 ** 3):.2f} GB"
        disk_avail = f"{disk.total / (1024 ** 3):.2f} GB"

        return {
            'CPU': f"{cpu_percent:.1f}%",
            'RAM': f"{ram_used} / {ram_avail}",
            'Disk': f"{disk_used} / {disk_avail}",
            'Last Update': datetime.now().strftime("%H:%M:%S")
        }

    def stop(self):
        """Останавливает цикл выполнения."""
        self._running = False
