#!/usr/bin/env python3
"""
Redfin Home Value Scraper
Scrapes the home value from a Redfin property listing page using headless Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chrome_driver_manager import ChromeDriverManager
from link_loader import LinkLoader
import time
import platform

def scrape_redfin_home_value(url, driver=None):
    """
    Scrape the home value from a Redfin property page
    
    Args:
        url (str): The Redfin property URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance. If None, creates a new one.
        
    Returns:
        str: The home value as a string, or None if not found
    """
    # Track if we created the driver (so we know whether to close it)
    driver_created = driver is None
    
    if driver is None:
        driver = ChromeDriverManager.create_driver()
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load and the price element to be present
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.statsValue.price"))
        )
        
        # Extract the text
        home_value = price_element.text.strip()
        
        print(f"Home value found: {home_value}")
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
    
    # Scrape the home value
    home_value = scrape_redfin_home_value(LinkLoader.redfin)
    
    if home_value:
        print(f"\n✓ Successfully scraped home value: {home_value}")
        
        # Write the value to redfin.txt
        try:
            with open("redfin.txt", "w") as f:
                f.write(home_value)
            print(f"✓ Home value saved to redfin.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape home value")

if __name__ == "__main__":
    main()
