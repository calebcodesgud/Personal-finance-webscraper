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

REM Check if required files exist
if not exist "run_scrapers.py" (
    echo ERROR: run_scrapers.py not found
    echo Please ensure all scraper files are in the same directory
    pause
    exit /b 1
)

if not exist "redfin_scraper.py" (
    echo ERROR: redfin_scraper.py not found
    pause
    exit /b 1
)

if not exist "zillow_scraper.py" (
    echo ERROR: zillow_scraper.py not found
    pause
    exit /b 1
)

if not exist "realtor_scraper.py" (
    echo ERROR: realtor_scraper.py not found
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
