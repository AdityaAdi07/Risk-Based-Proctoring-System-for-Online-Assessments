import logging
import os

LOG_FILE = os.path.join(os.getenv("APPDATA", "C:\\Logs"), "user_sdk.log")

def setup_logger():
    """Configures logging for the application."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def log_event(level, message):
    """Logs an event at the specified level."""
    if level.lower() == "info":
        logging.info(message)
    elif level.lower() == "warning":
        logging.warning(message)
    elif level.lower() == "error":
        logging.error(message)
    else:
        logging.debug(message)

# Initialize logger
setup_logger()

# Example Usage
if __name__ == "__main__":
    log_event("info", "Application started")
    log_event("error", "This is a test error")
    print(f"Logs saved to {LOG_FILE}")
