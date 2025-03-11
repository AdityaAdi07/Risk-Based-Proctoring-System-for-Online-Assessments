import ctypes
import winreg

def apply_os_restrictions():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)

        print("Task Manager disabled successfully.")
    except Exception as e:
        print(f"Error disabling Task Manager: {e}")

    # Alternative: Low-level Hook for Blocking Alt+Tab Instead of BlockInput
    try:
        ctypes.windll.user32.BlockInput(True)  # Be careful, this blocks all input
        print("Input blocked (Alt+Tab, etc.)")
    except Exception as e:
        print(f"Error blocking input: {e}")

def restore_os_restrictions():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)

        print("Task Manager enabled successfully.")
    except Exception as e:
        print(f"Error enabling Task Manager: {e}")

    try:
        ctypes.windll.user32.BlockInput(False)
        print("Input unblocked.")
    except Exception as e:
        print(f"Error unblocking input: {e}")
