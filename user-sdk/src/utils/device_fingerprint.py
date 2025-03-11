import hashlib
import uuid
import platform
import os
import subprocess
import winreg

def get_disk_serial():
    """Fetches the system's primary disk serial number (Windows Registry + WMIC Fallback)."""
    if platform.system() != "Windows":
        return "Non-Windows-System"

    try:
        # Try reading from Windows Registry
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Disk\Enum") as key:
            serial_number, _ = winreg.QueryValueEx(key, "0")
            return serial_number
    except Exception:
        pass  # If registry method fails, fallback to WMIC

    try:
        # Fallback to WMIC command
        result = subprocess.run(["wmic", "diskdrive", "get", "serialnumber"], capture_output=True, text=True)
        serial_numbers = result.stdout.split("\n")[1:]  # Skip header line
        serial_numbers = [s.strip() for s in serial_numbers if s.strip()]
        return serial_numbers[0] if serial_numbers else "UnknownDiskSerial"
    except Exception:
        return "UnknownDiskSerial"

def get_mac_address():
    """Fetches the system's primary MAC address (ignoring virtual adapters)."""
    try:
        result = subprocess.run(["getmac"], capture_output=True, text=True)
        mac_addresses = [line.split()[0] for line in result.stdout.split("\n") if "-" in line]
        return mac_addresses[0] if mac_addresses else hex(uuid.getnode())  # Fallback to `uuid.getnode()`
    except Exception:
        return hex(uuid.getnode())

def generate_fingerprint():
    """Generates a unique fingerprint based on system attributes (Windows only)."""
    if platform.system() != "Windows":
        return "Fingerprinting Not Supported on This OS"

    try:
        system_info = f"""
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        MAC Address: {get_mac_address()}
        Disk Serial: {get_disk_serial()}
        OS Edition: {platform.win32_edition() if hasattr(platform, 'win32_edition') else 'Unknown'}
        OS Version: {platform.version()}
        User: {os.getenv('USERNAME', 'UnknownUser')}
        """
        return hashlib.sha256(system_info.encode()).hexdigest()
    except Exception as e:
        return f"Error generating fingerprint: {e}"

if __name__ == "__main__":
    print(f"🔑 Device Fingerprint: {generate_fingerprint()}")
