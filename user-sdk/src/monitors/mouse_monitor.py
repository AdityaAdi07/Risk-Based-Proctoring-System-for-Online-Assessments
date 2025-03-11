import threading
import ctypes
from PyQt5.QtCore import QObject, pyqtSignal

class MouseMonitor(QObject):
    update_signal = pyqtSignal(dict)

    def __init__(self, config):
        super().__init__()
        self.user32 = ctypes.windll.user32
        self.running = False
        self.threshold = config['mouse_sensitivity']

    def get_position(self):
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
        pt = POINT()
        self.user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.monitor)
        thread.daemon = True
        thread.start()

    def monitor(self):
        last_pos = self.get_position()
        while self.running:
            current_pos = self.get_position()
            dx = abs(current_pos[0] - last_pos[0])
            dy = abs(current_pos[1] - last_pos[1])
            
            if dx + dy > self.threshold:
                self.update_signal.emit({
                    'type': 'mouse',
                    'data': {'speed': dx + dy}
                })
            last_pos = current_pos