import logging
import os

# Ensure log directory exists
log_dir = os.getenv("APPDATA", "C:\\Logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # Creates C:\Logs if it doesn’t exist

LOG_FILE = os.path.join(log_dir, "user_sdk.log")

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
    logger = logging.getLogger()
    if level.lower() == "info":
        logger.info(message)
    elif level.lower() == "warning":
        logger.warning(message)
    elif level.lower() == "error":
        logger.error(message)
    else:
        logger.debug(message)

# Initialize logger
setup_logger()

# Example Usage
if __name__ == "__main__":
    log_event("info", "✅ Application started successfully")
    log_event("warning", "⚠️ This is a warning message")
    log_event("error", "❌ This is an error message")
    print(f"📁 Logs saved to: {LOG_FILE}")
