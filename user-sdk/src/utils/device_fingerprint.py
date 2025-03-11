import hashlib
import uuid
import platform
import os
import winreg

def get_disk_serial():
    """Fetches the system's primary disk serial number from Windows Registry."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Disk\Enum") as key:
            serial_number, _ = winreg.QueryValueEx(key, "0")
            return serial_number
    except Exception:
        return "UnknownDiskSerial"

def generate_fingerprint():
    """Generates a unique fingerprint based on system attributes (Windows only)."""
    try:
        system_info = f"""
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        Node: {uuid.getnode()}
        OS Edition: {platform.win32_edition()}
        OS Version: {platform.version()}
        Disk Serial: {get_disk_serial()}
        User: {os.getenv('USERNAME', 'UnknownUser')}
        """
        return hashlib.sha256(system_info.encode()).hexdigest()
    except Exception as e:
        return f"Error generating fingerprint: {e}"

if __name__ == "__main__":
    print(generate_fingerprint())
