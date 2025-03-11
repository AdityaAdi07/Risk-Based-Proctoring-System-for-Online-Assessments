import threading
import ctypes
from PyQt5.QtCore import QObject, pyqtSignal

class KeyboardMonitor(QObject):
    update_signal = pyqtSignal(dict)

    def __init__(self, config):
        super().__init__()
        self.user32 = ctypes.windll.user32
        self.running = False
        self.threshold = config['keyboard_sensitivity']
        self.key_count = 0

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.monitor)
        thread.daemon = True
        thread.start()

    def monitor(self):
        while self.running:
            for key in range(0x08, 0xFF):  # Virtual key codes range
                if self.user32.GetAsyncKeyState(key) & 0x8000:
                    self.key_count += 1
                    if self.key_count >= self.threshold:
                        self.update_signal.emit({
                            'type': 'keyboard',
                            'data': {'keystrokes': self.key_count}
                        })
                        self.key_count = 0
