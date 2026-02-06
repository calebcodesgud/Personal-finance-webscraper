#!/usr/bin/env python3
"""
Bitnodes.io Bitcoin Nodes Scraper
Scrapes the total number of Bitcoin nodes from bitnodes.io using headless Selenium
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

def scrape_bitcoin_node_count(url, driver=None):
    """
    Scrape the total number of Bitcoin nodes from bitnodes.io
    
    Args:
        url (str): The bitnodes.io URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance. If None, creates a new one.
        
    Returns:
        str: The total number of Bitcoin nodes as a string, or None if not found
    """
    # Track if we created the driver (so we know whether to close it)
    driver_created = driver is None
    
    if driver is None:
        driver = ChromeDriverManager.create_driver()
    
    try:
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for the page to load and the node count element to be present
        wait = WebDriverWait(driver, 15)
        
        # Find the <a> tag with href="/nodes/"
        node_count_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="."]'))
        )
        
        # Extract the text
        node_count = node_count_element.text.strip()
        
        print(f"Total Bitcoin nodes found: {node_count}")
        return node_count
        
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
    
    # Scrape the total Bitcoin node count
    node_count = scrape_bitcoin_node_count(LinkLoader.bitnodes)
    
    if node_count:
        print(f"\n✓ Successfully scraped Bitcoin node count: {node_count}")
        
        # Write the value to bitnodes.txt
        try:
            with open("bitnodes.txt", "w") as f:
                f.write(node_count)
            print(f"✓ Bitcoin node count saved to bitnodes.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape Bitcoin node count")

if __name__ == "__main__":
    main()
