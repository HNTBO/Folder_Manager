@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo File Counter for Folder Manager
echo.

REM Resolve script directory (so this works from any location)
set "SCRIPT_DIR=%~dp0"

REM Find a Python interpreter (prefer python, fallback to py -3)
set "PYTHON="
where python >nul 2>&1 && set "PYTHON=python"
if not defined PYTHON (
    where py >nul 2>&1 && set "PYTHON=py -3"
)
if not defined PYTHON (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://python.org
    echo.
    pause
    exit /b 1
)

REM Get folder path from user if not provided
if "%~1"=="" (
    echo Usage:
    echo   count_files.bat [options] [folder_path]
    echo.
    echo Options:
    echo   --detailed    Show breakdown by type and folder
    echo   --size        Show total size and per-type sizes
    echo.
    echo Examples:
    echo   count_files.bat C:\Users\YourName\Documents
    echo   count_files.bat --detailed Test_Folder_Structure
    echo   count_files.bat --size --detailed .
    echo.
    set /p folder_path="Enter folder path (or press Enter for current directory): "
    if "!folder_path!"=="" set "folder_path=."
    "%PYTHON%" "%SCRIPT_DIR%count_files.py" %* "!folder_path!"
) else (
    "%PYTHON%" "%SCRIPT_DIR%count_files.py" %*
)

echo.
pause
endlocal
