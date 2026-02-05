# Home Value Scraper

Automated scraper to get home values from Redfin, Zillow, and Realtor.com for the property, as well as Bitcoin and Ethereum node counts.

## Files Included

### Scrapers
- `redfin_scraper.py` - Scrapes home value from Redfin
- `zillow_scraper.py` - Scrapes Zestimate from Zillow
- `realtor_scraper.py` - Scrapes estimated home value from Realtor.com
- `bitnodes_scraper.py` - Scrapes Bitcoin node count from Bitnodes.io
- `etherscan_scraper.py` - Scrapes Ethereum node count from Etherscan.io

### Core Files
- `run_scrapers.py` - Main script that runs all five scrapers
- `chrome_driver_manager.py` - Manages Chrome WebDriver instances
- `link_loader.py` - Loads scraper URLs from configuration file
- `date_gate.py` - Prevents running scrapers more than once per day
- `links.json` - Configuration file containing all scraper URLs

### Launchers
- `run_scrapers.bat` - Windows executable launcher
- `run_scrapers.sh` - Ubuntu/Linux executable launcher

### Other
- `requirements.txt` - Python dependencies
- `LICENSE` - License information

## Requirements

### Both Platforms
- Python 3.7 or higher
- Chrome/Chromium browser
- Chromedriver (Chrome WebDriver)

## Installation

### Windows Installation

1. **Install Python**
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: Open Command Prompt and type `python --version`

2. **Install Chrome**
   - Download from https://www.google.com/chrome/

3. **Install Chromedriver**
   - Download from https://chromedriver.chromium.org/downloads
   - Download version matching your Chrome version
   - Extract `chromedriver.exe`
   - Add to PATH or place in the same folder as the scripts

4. **Install Python Dependencies**
   ```cmd
   cd path\to\scraper\folder
   pip install -r requirements.txt
   ```

### Ubuntu/Linux Installation

1. **Install Python 3** (usually pre-installed)
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install Chromium Browser**
   ```bash
   sudo apt install chromium-browser
   ```

3. **Install Chromedriver**
   ```bash
   sudo apt install chromium-chromedriver
   ```
   
   Or manually download:
   ```bash
   # Check your chromium version first
   chromium-browser --version
   
   # Download matching chromedriver from:
   # https://chromedriver.chromium.org/downloads
   
   # Extract and install
   sudo mv chromedriver /usr/bin/
   sudo chmod +x /usr/bin/chromedriver
   ```

4. **Install Python Dependencies**
   ```bash
   cd /path/to/scraper/folder
   pip3 install -r requirements.txt
   ```

## Configuration

All scraper URLs are stored in `links.json`. To update URLs for any scraper, simply edit this file:

```json
{
  "redfin": "https://www.redfin.com/OH/Columbus/285-E-Lane-Ave-43201/home/100731813",
  "zillow": "https://www.zillow.com/homedetails/285-E-Lane-Ave-Columbus-OH-43201/33844741_zpid/",
  "realtor": "https://www.realtor.com/myhome/285-E-Lane-Ave_Columbus_OH_43201_M40304-63511/prepare-to-sell",
  "bitnodes": "https://bitnodes.io/nodes/",
  "etherscan": "https://etherscan.io/nodetracker#"
}
```

No code changes are needed when updating URLs - just modify the JSON file.

## Usage

### Windows

**Double-click** `run_scrapers.bat`

Or from Command Prompt:
```cmd
run_scrapers.bat
```

### Ubuntu/Linux

First, make the script executable:
```bash
chmod +x run_scrapers.sh
```

Then run it:
```bash
./run_scrapers.sh
```

Or:
```bash
bash run_scrapers.sh
```

### Manual Python Execution

You can also run the Python script directly on both platforms:

Windows:
```cmd
python run_scrapers.py
```

Ubuntu/Linux:
```bash
python3 run_scrapers.py
```

## Output

The scraper creates five text files:
- `redfin.txt` - Contains the home value from Redfin
- `zillow.txt` - Contains the Zestimate from Zillow
- `realtor.txt` - Contains the estimated home value from Realtor.com
- `bitnodes.txt` - Contains the Bitcoin node count
- `etherscan.txt` - Contains the Ethereum node count

## Running Individual Scrapers

You can also run each scraper independently:

```bash
# Redfin only
python redfin_scraper.py

# Zillow only
python zillow_scraper.py

# Realtor.com only
python realtor_scraper.py

# Bitnodes only
python bitnodes_scraper.py

# Etherscan only
python etherscan_scraper.py
```

Each individual scraper will automatically load its URL from `links.json`.

## Date Gate Feature

The scraper includes a date gate feature that prevents it from running more than once per day. If you try to run the scraper multiple times in the same day, it will skip the operation and display "Already ran today. Skipping operation."

The last run date is stored in a file called `last_success`. To force the scraper to run again on the same day, simply delete this file.

## Troubleshooting

### "chromedriver not found"
- Make sure chromedriver is installed and in your system PATH
- On Windows: Add chromedriver.exe location to PATH or copy to script folder
- On Ubuntu: Run `sudo apt install chromium-chromedriver`

### "Module not found: selenium"
- Install dependencies: `pip install -r requirements.txt` (Windows) or `pip3 install -r requirements.txt` (Ubuntu)

### "Configuration file 'links.json' not found"
- Make sure `links.json` is in the same directory as the scraper scripts
- The file should contain valid JSON with all five URL entries

### Scraper returns no value
- The website structure may have changed
- Check your internet connection
- Try running in non-headless mode to see what's happening (edit `chrome_driver_manager.py` and remove `--headless` argument)

### Chrome/Chromium not found
- Make sure Chrome/Chromium is installed
- On Ubuntu: `sudo apt install chromium-browser`
- On Windows: Download from google.com/chrome

## Notes

- The scrapers run in headless mode (no visible browser window)
- Each scrape takes 10-20 seconds to complete
- All scrapers share a single Chrome driver instance for efficiency
- Website structures may change over time, requiring script updates
- URLs are centrally managed in `links.json` for easy configuration
