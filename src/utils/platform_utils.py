import platform
import os
import ctypes

def get_os_type():
    """Returns 'Windows', 'Linux', or 'Darwin'."""
    return platform.system()

def is_admin():
    """Checks for administrative privileges."""
    try:
        if get_os_type() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except AttributeError:
        return False
