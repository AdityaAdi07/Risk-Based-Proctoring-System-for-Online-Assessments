import sys
import json
import ctypes
import threading
import os
from utils.keyLogger import KeyLogger
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from monitors.mouse_monitor import MouseMonitor
from monitors.keyboard_monitor import KeyboardMonitor
from monitors.focus_monitor import FocusMonitor
from os_controls.windows_lockdown import apply_os_restrictions
from utils.device_fingerprint import generate_fingerprint  # Ensure correct function name

def run_as_admin():
    """Request admin privileges if not already running as admin."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return  # Already running as admin, continue normally

    # Relaunch with admin rights
    print("🔴 Restarting with admin privileges...")
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

    if result <= 32:
        print("❌ Error: Failed to restart with admin privileges.")
        sys.exit(1)  # Exit with error if relaunch failed

    sys.exit(0)  # Exit the original (non-admin) process

class ProctoringApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()
        self.config = self.load_config()
        
        # Initialize components
        self.init_ui()
        self.init_monitors()
        self.start_logging()
        apply_os_restrictions()

    def load_config(self):
        """Loads application configuration from settings.json."""
        config_path = os.path.join(os.path.dirname(__file__), "config", "settings.json")
        if not os.path.exists(config_path):
            print(f"❌ Error: Configuration file not found at '{config_path}'")
            sys.exit(1)

        with open(config_path, "r") as f:
            return json.load(f)

    def init_ui(self):
        """Initialize system tray UI."""
        self.tray.setIcon(QIcon('icon.png'))
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def init_monitors(self):
        """Start monitoring components."""
        MouseMonitor(self.config).start()
        KeyboardMonitor(self.config).start()
        FocusMonitor(self.config).start()  

    def start_logging(self):
        """Starts the keylogger in a background thread."""
        keylogger = KeyLogger()  # Store KeyLogger instance
        keylogger_thread = threading.Thread(target=keylogger.start_logging, daemon=True)
        keylogger_thread.start()

    def exit_app(self):
        """Exit the application."""
        print("🔴 Exiting Proctoring App...")
        sys.exit(0)

    def run(self):
        """Run the application."""
        print("🚀 Proctoring App Running...")
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    run_as_admin()  # Ensure script runs with admin privileges

    fingerprint = generate_fingerprint()  # Use correct function
    print(f"🔑 Device Fingerprint: {fingerprint}")

    app = ProctoringApp()
    app.run()
