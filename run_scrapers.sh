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

# Run the scraper
echo "Running scrapers..."
echo ""
python3 run_scrapers.py

# Capture exit code
exit_code=$?
sleep 2
exit $exit_code
