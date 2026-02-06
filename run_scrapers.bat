@echo off
REM Home Value Scraper - Windows Launcher
REM This batch file runs the combined scraper on Windows

echo ============================================================
echo Home Value Scraper - Windows
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Run the scraper
echo Running scrapers...
echo.
python run_scrapers.py

REM Pause to see results
echo.
echo ============================================================
pause
