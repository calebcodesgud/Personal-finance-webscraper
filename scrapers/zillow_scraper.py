#!/usr/bin/env python3
"""
Zillow Home Value Scraper
Scrapes the Zestimate value from a Zillow property listing page using headless Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.chrome_driver_manager import ChromeDriverManager
from util.link_loader import LinkLoader
import time
import platform

def scrape_zillow_zestimate(url, driver=None):
    """
    Scrape the Zestimate value from a Zillow property page
    
    Args:
        url (str): The Zillow property URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance. If None, creates a new one.
        
    Returns:
        str: The Zestimate value as a string, or None if not found
    """
    # Track if we created the driver (so we know whether to close it)
    driver_created = driver is None
    
    if driver is None:
        driver = ChromeDriverManager.create_driver()
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load and the Zestimate element to be present
        wait = WebDriverWait(driver, 15)
        
        # Find the p tag with data-testid="primary-zestimate"
        zestimate_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p[data-testid="primary-zestimate"]'))
        )
        
        # Extract the text
        home_value = zestimate_element.text.strip()
        
        print(f"Zestimate value found: {home_value}")
        return home_value
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
        
    finally:
        # Clean up - close the browser only if we created it
        if driver_created and driver:
            driver.quit()

def main():
    """Main function to run the scraper"""
    # Load links from configuration
    LinkLoader.load()
    
    # Scrape the Zestimate value
    home_value = scrape_zillow_zestimate(LinkLoader.zillow)
    
    if home_value:
        print(f"\n✓ Successfully scraped Zestimate: {home_value}")
        
        # Write the value to zillow.txt
        try:
            with open("zillow.txt", "w") as f:
                f.write(home_value)
            print(f"✓ Zestimate saved to zillow.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape Zestimate")

if __name__ == "__main__":
    main()
