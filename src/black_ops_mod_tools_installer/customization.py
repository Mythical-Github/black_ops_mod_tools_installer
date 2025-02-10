import os


def enable_vt100():
    """Enable VT100 escape codes in the Windows Command Prompt."""
    # Check if VT100 is already enabled
    query_command = 'reg query HKCU\\Console /v VirtualTerminalLevel 2>nul'
    result = os.popen(query_command).read()
    if "0x1" not in result:  # If not enabled, set the registry key
        os.system('reg add HKCU\\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul')
