@echo off
cd /d %~dp0

title Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed!
    echo Download it here: https://www.python.org/downloads
    echo Ensure it is added to PATH during installation.
    pause
    exit
)

title Updating Pip...
python -m pip install --upgrade pip --quiet

title Downloading libraries...

for %%A in (
    "requests"
    "pycryptodome"
    "discord.py"
    "opencv-python"
    "pyperclip"
    "pillow"
    "uuid"
    "imageio"
    "pywin32"
    "pynput"
    "pyaudio"
    "wave"
) do (
    echo Checking %%~A...
    python -c "import %%~A" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing %%~A...
        python -m pip install %%~A --quiet
    )
)

cls
title Libraries installed successfully.
echo All modules installed and up-to-date.
pause
exit
