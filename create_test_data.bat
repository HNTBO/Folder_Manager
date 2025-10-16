@echo off
echo Creating Test Data for Folder Manager...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.x from https://python.org
    pause
    exit /b 1
)

echo Running test data generator...
echo.

set /p SEED=Enter seed for deterministic generation (leave blank for random): 

REM Run the test data generator with or without seed
if "%SEED%"=="" (
    python create_test_data.py
 ) else (
    python create_test_data.py --seed "%SEED%"
 )

echo.
echo Test data creation completed!
echo You can now test your Folder Manager application.
echo.
pause
