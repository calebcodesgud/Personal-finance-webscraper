#!/usr/bin/env python3
"""
Etherscan.io Ethereum Nodes Scraper
Scrapes the total number of Ethereum nodes from etherscan.io using headless Selenium
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
import re

def scrape_ethereum_node_count(url, driver=None):
    """
    Scrape the total number of Ethereum nodes from etherscan.io
    
    Args:
        url (str): The etherscan.io nodetracker URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance. If None, creates a new one.
        
    Returns:
        str: The total number of Ethereum nodes as a string, or None if not found
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
        
        # Try multiple strategies to find the element
        node_count = None
        
        try:
            # Strategy 1: Look for p tag with class text-muted
            print("Attempting strategy 1: p.text-muted with 'Total' and 'nodes found'...")
            node_count_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//p[contains(@class, "text-muted") and contains(., "Total") and contains(., "nodes found")]'))
            )
            strong_element = node_count_element.find_element(By.TAG_NAME, "strong")
            node_count = strong_element.text.strip()
            print(f"Strategy 1 successful. Full text: {node_count_element.text.strip()}")
        except Exception as e1:
            print(f"Strategy 1 failed: {str(e1)}")
            
            try:
                # Strategy 2: Just look for any p tag with "nodes found"
                print("Attempting strategy 2: any p tag with 'nodes found'...")
                node_count_element = driver.find_element(By.XPATH, '//p[contains(., "nodes found")]')
                strong_element = node_count_element.find_element(By.TAG_NAME, "strong")
                node_count = strong_element.text.strip()
                print(f"Strategy 2 successful. Full text: {node_count_element.text.strip()}")
            except Exception as e2:
                print(f"Strategy 2 failed: {str(e2)}")
                
                try:
                    # Strategy 3: Look for strong tag near "Total" text
                    print("Attempting strategy 3: looking for pattern in page source...")
                    page_source = driver.page_source
                    import re
                    match = re.search(r'Total\s*<strong[^>]*>([^<]+)</strong>\s*nodes found', page_source)
                    if match:
                        node_count = match.group(1).strip()
                        print(f"Strategy 3 successful. Found: {node_count}")
                    else:
                        print("Strategy 3 failed: pattern not found in page source")
                except Exception as e3:
                    print(f"Strategy 3 failed: {str(e3)}")
        
        if not node_count:
            raise Exception("All strategies failed to find node count")
        
        print(f"Total Ethereum nodes found: {node_count}")
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
    
    # Scrape the total Ethereum node count
    node_count = scrape_ethereum_node_count(LinkLoader.etherscan)
    
    if node_count:
        print(f"\n✓ Successfully scraped Ethereum node count: {node_count}")
        
        # Write the value to etherscan.txt
        try:
            with open("etherscan.txt", "w") as f:
                f.write(node_count)
            print(f"✓ Ethereum node count saved to etherscan.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape Ethereum node count")

if __name__ == "__main__":
    main()
