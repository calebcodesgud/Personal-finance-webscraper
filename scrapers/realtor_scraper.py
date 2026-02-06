#!/usr/bin/env python3
"""
Realtor.com Home Value Scraper
Scrapes the estimated home value from a Realtor.com property listing page using headless Selenium
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

def scrape_realtor_home_value(url, driver=None):
    """
    Scrape the estimated home value from a Realtor.com property page
    
    Args:
        url (str): The Realtor.com property URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance. If None, creates a new one.
        
    Returns:
        str: The estimated home value as a string, or None if not found
    """
    # Track if we created the driver (so we know whether to close it)
    driver_created = driver is None
    
    if driver is None:
        driver = ChromeDriverManager.create_driver()
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load and the home value element to be present
        wait = WebDriverWait(driver, 15)
        
        # Find the h2 tag with data-testid="estimated-home-value-currency"
        home_value_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2[data-testid="estimated-home-value-currency"]'))
        )
        
        # Extract the text
        home_value = home_value_element.text.strip()
        
        print(f"Estimated home value found: {home_value}")
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
    
    # Scrape the estimated home value
    home_value = scrape_realtor_home_value(LinkLoader.realtor)
    
    if home_value:
        print(f"\n✓ Successfully scraped estimated home value: {home_value}")
        
        # Write the value to realtor.txt
        try:
            with open("realtor.txt", "w") as f:
                f.write(home_value)
            print(f"✓ Estimated home value saved to realtor.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape estimated home value")

if __name__ == "__main__":
    main()
