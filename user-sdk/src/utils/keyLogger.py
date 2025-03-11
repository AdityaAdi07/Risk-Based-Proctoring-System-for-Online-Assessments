import json
import os
import datetime
from pynput import keyboard
from utils.device_fingerprint import generate_fingerprint

LOG_FILE = "keystrokes.json"

class KeyLogger:
    def __init__(self):
        self.device_fingerprint = generate_fingerprint()
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_id = f"{self.device_fingerprint}_{self.start_time.replace(':', '-')}"
        self.keystrokes = self.load_existing_data()

    def load_existing_data(self):
        """Loads existing keystroke data, ensuring sessions are stored separately."""
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}

        return {}

    def on_press(self, key):
        """Records each key press and updates count."""
        try:
            key_str = key.char if key.char else str(key)
        except AttributeError:
            key_str = str(key)

        # Store key presses in a structured format per session
        if self.session_id not in self.keystrokes:
            self.keystrokes[self.session_id] = {
                "Device Fingerprint": self.device_fingerprint,
                "Session Start Time": self.start_time,
                "Keystrokes": {}
            }

        if key_str in self.keystrokes[self.session_id]["Keystrokes"]:
            self.keystrokes[self.session_id]["Keystrokes"][key_str] += 1
        else:
            self.keystrokes[self.session_id]["Keystrokes"][key_str] = 1

        self.save_data()

    def save_data(self):
        """Saves keystroke data incrementally to JSON file."""
        with open(LOG_FILE, "w") as f:
            json.dump(self.keystrokes, f, indent=4)

    def start_logging(self):
        """Starts listening for keystrokes."""
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    logger = KeyLogger()
    logger.start_logging()
