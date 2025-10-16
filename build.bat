@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo Building Folder Manager Application...
echo.

REM Resolve script directory
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%" >nul

REM Find Python interpreter (prefer python, fallback to py -3)
set "PYTHON="
where python >nul 2>&1 && set "PYTHON=python"
if not defined PYTHON (
    where py >nul 2>&1 && set "PYTHON=py -3"
)
if not defined PYTHON (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://python.org
    pause
    popd >nul
    exit /b 1
)

REM Option to skip dependency install: build.bat --skip-pip
set "SKIP_PIP="
if /I "%~1"=="--skip-pip" set "SKIP_PIP=1"

if not defined SKIP_PIP (
    echo Installing/validating dependencies...
    "%PYTHON%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        popd >nul
        exit /b 1
    )
    echo Dependencies installed successfully.
    echo.
)

REM Ensure output folders exist
if not exist "logs" mkdir logs
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo Building executable...
echo.

"%PYTHON%" -m PyInstaller --noconfirm --onefile --windowed ^
  --name "FolderManager" ^
  --distpath "dist" --workpath "build" --specpath "build" ^
  folder_manager.py

if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    popd >nul
    exit /b 1
)

echo.
echo Build completed successfully!
echo.
echo The executable can be found in the 'dist' folder:
echo %cd%\dist\FolderManager.exe
echo.
echo You can now run the application by double-clicking the .exe file.
echo.
popd >nul
pause
endlocal
