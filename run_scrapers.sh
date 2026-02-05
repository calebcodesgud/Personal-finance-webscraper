#!/bin/bash
# Home Value Scraper - Linux/Ubuntu Launcher
# This shell script runs the combined scraper on Ubuntu/Linux

echo "============================================================"
echo "Home Value Scraper - Ubuntu/Linux"
echo "============================================================"
echo ""

cd ~/MEGA/scraper

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: sudo apt install python3"
    exit 1
fi

# Check if required files exist
if [ ! -f "run_scrapers.py" ]; then
    echo "ERROR: run_scrapers.py not found"
    echo "Please ensure all scraper files are in the same directory"
    exit 1
fi

if [ ! -f "redfin_scraper.py" ]; then
    echo "ERROR: redfin_scraper.py not found"
    exit 1
fi

if [ ! -f "zillow_scraper.py" ]; then
    echo "ERROR: zillow_scraper.py not found"
    exit 1
fi

if [ ! -f "realtor_scraper.py" ]; then
    echo "ERROR: realtor_scraper.py not found"
    exit 1
fi

# Run the scraper
echo "Running scrapers..."
echo ""
python3 run_scrapers.py

# Capture exit code
exit_code=$?
sleep 2
exit $exit_code
