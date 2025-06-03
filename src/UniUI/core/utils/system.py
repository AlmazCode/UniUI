import platform

def get_refresh_rate():
    system = platform.system()

    if system == "Windows":
        import ctypes

        class DEVMODE(ctypes.Structure):
            _fields_ = [
                ("dmDeviceName", ctypes.c_wchar * 32),
                ("dmSpecVersion", ctypes.c_ushort),
                ("dmDriverVersion", ctypes.c_ushort),
                ("dmSize", ctypes.c_ushort),
                ("dmDriverExtra", ctypes.c_ushort),
                ("dmFields", ctypes.c_ulong),
                ("dmPosition_x", ctypes.c_long),
                ("dmPosition_y", ctypes.c_long),
                ("dmDisplayOrientation", ctypes.c_ulong),
                ("dmDisplayFixedOutput", ctypes.c_ulong),
                ("dmColor", ctypes.c_short),
                ("dmDuplex", ctypes.c_short),
                ("dmYResolution", ctypes.c_short),
                ("dmTTOption", ctypes.c_short),
                ("dmCollate", ctypes.c_short),
                ("dmFormName", ctypes.c_wchar * 32),
                ("dmLogPixels", ctypes.c_ushort),
                ("dmBitsPerPel", ctypes.c_ulong),
                ("dmPelsWidth", ctypes.c_ulong),
                ("dmPelsHeight", ctypes.c_ulong),
                ("dmDisplayFlags", ctypes.c_ulong),
                ("dmDisplayFrequency", ctypes.c_ulong),
                ("dmICMMethod", ctypes.c_ulong),
                ("dmICMIntent", ctypes.c_ulong),
                ("dmMediaType", ctypes.c_ulong),
                ("dmDitherType", ctypes.c_ulong),
                ("dmReserved1", ctypes.c_ulong),
                ("dmReserved2", ctypes.c_ulong),
                ("dmPanningWidth", ctypes.c_ulong),
                ("dmPanningHeight", ctypes.c_ulong),
            ]

        user32 = ctypes.windll.user32
        devmode = DEVMODE()
        devmode.dmSize = ctypes.sizeof(DEVMODE)
        if user32.EnumDisplaySettingsW(None, -1, ctypes.byref(devmode)):
            return devmode.dmDisplayFrequency
        else:
            return None

    elif system == "Linux":
        import subprocess
        import re

        try:
            output = subprocess.check_output("xrandr", text=True)
            match = re.search(r'(\d+\.\d+)\*', output)
            if match:
                return float(match.group(1))
        except Exception:
            pass
        return None

    # elif system == "Darwin":
    #     try:
    #         import Quartz # type: ignore
    #         display = Quartz.CGMainDisplayID()
    #         mode = Quartz.CGDisplayCopyDisplayMode(display)
    #         return Quartz.CGDisplayModeGetRefreshRate(mode)
    #     except ImportError:
    #         return None

    else:
        return None