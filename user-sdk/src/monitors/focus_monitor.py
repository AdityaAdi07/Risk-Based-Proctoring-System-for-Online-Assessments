import threading
from PyQt5.QtCore import QObject, pyqtSignal
import time
import win32gui

class FocusMonitor(QObject):
    update_signal = pyqtSignal(dict)

    def __init__(self, config):
        super().__init__()
        self.running = False
        self.interval = config["focus_check_interval"]  # Get interval from settings

    def get_active_window(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.monitor)
        thread.daemon = True
        thread.start()

    def monitor(self):
        last_window = self.get_active_window()
        while self.running:
            time.sleep(self.interval)
            current_window = self.get_active_window()
            if current_window != last_window:
                self.update_signal.emit({
                    "type": "focus",
                    "data": {"window": current_window}
                })
            last_window = current_window
