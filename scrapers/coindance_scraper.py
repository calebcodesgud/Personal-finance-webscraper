#!/usr/bin/env python3
"""
Coin.Dance Bitcoin Nodes Scraper
Scrapes the total number of Bitcoin nodes from coin.dance/nodes using headless Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util.chrome_driver_manager import ChromeDriverManager
from util.link_loader import LinkLoader


def scrape_bitcoin_node_count(url, driver=None):
    """
    Scrape the total number of Bitcoin nodes from coin.dance/nodes

    The node count is embedded in a <div> like:
        There are currently <strong style="color:#666666">24293</strong>* public nodes...

    Args:
        url (str): The coin.dance nodes URL
        driver (webdriver.Chrome, optional): Existing Chrome driver instance.
                                             If None, creates a new one.

    Returns:
        str: The total number of Bitcoin nodes as a string, or None if not found
    """
    driver_created = driver is None

    if driver is None:
        driver = ChromeDriverManager.create_driver()

    try:
        print(f"Navigating to: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        # Wait until the <strong> inside the node-count div is present.
        # The parent div carries a data-hasqtip attribute whose title mentions
        # "Total node count"; we locate the <strong> directly inside it.
        node_count_element = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@oldtitle='Total node count does not include duplicate and non-listening nodes.']//strong"
            ))
        )

        node_count = node_count_element.text.strip()

        print(f"Total Bitcoin nodes found: {node_count}")
        return node_count

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

    finally:
        if driver_created and driver:
            driver.quit()


def main():
    """Main function to run the scraper"""
    # Load links from configuration
    LinkLoader.load()

    # Scrape the total Bitcoin node count
    node_count = scrape_bitcoin_node_count(LinkLoader.coindance)

    if node_count:
        print(f"\n✓ Successfully scraped Bitcoin node count: {node_count}")

        # Write the value to coindance.txt
        try:
            with open("coindance.txt", "w") as f:
                f.write(node_count)
            print("✓ Bitcoin node count saved to coindance.txt")
        except Exception as e:
            print(f"✗ Error writing to file: {str(e)}")
    else:
        print("\n✗ Failed to scrape Bitcoin node count")


if __name__ == "__main__":
    main()
