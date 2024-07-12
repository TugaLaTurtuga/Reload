@echo off

REM Get the directory of the script
set SCRIPT_DIR=%~dp0

REM Function to run Update_screen.py in the background
:start_update_screen
if exist "%SCRIPT_DIR%Contents\Saves\Update_screen.py" (
    start /b python "%SCRIPT_DIR%Contents\Saves\Update_screen.py"
    set UPDATE_SCREEN_PID=%!
) else (
    echo Contents\Saves\Update_screen.py not found. Please check the path and try again.
    exit /b 1
)

REM Function to stop the Update_screen.py process
:stop_update_screen
if defined UPDATE_SCREEN_PID (
    taskkill /PID %UPDATE_SCREEN_PID% /F
)

call :start_update_screen

REM Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    REM Check if running in Administrator mode
    openfiles >nul 2>nul
    if %errorlevel% neq 0 (
        echo This script needs to be run as Administrator to install Python.
        pause
        exit /b 1
    )
    REM Installing Python using Chocolatey
    where choco >nul 2>nul
    if %errorlevel% neq 0 (
        echo Chocolatey is not installed. Installing Chocolatey...
        @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    )
    choco install -y python
) else (
    echo Python is already installed.
)

REM Upgrade pip
python -m pip install --upgrade pip

REM Install pygame and mutagen
python -m pip install pygame mutagen

call :stop_update_screen

REM Run the Main.py script
if exist "%SCRIPT_DIR%Contents\Main.py" (
    python "%SCRIPT_DIR%Contents\Main.py"
) else (
    echo Contents\Main.py not found. Please check the path and try again.
    exit /b 1
)

exit /b 0
