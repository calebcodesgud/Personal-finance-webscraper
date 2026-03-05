#!/usr/bin/env python3
"""
Combined Home Value and Node Count Scraper
Runs Redfin, Zillow, Realtor.com, Bitnodes, Coin.dance, and Etherscan scrapers.
Each scraper only runs if its corresponding entry is enabled in links.json.
"""

import sys
from scrapers.redfin_scraper import scrape_redfin_home_value
from scrapers.zillow_scraper import scrape_zillow_zestimate
from scrapers.realtor_scraper import scrape_realtor_home_value
from scrapers.bitnodes_scraper import scrape_bitcoin_node_count
from scrapers.coindance_scraper import scrape_bitcoin_node_count as scrape_coindance_node_count
from scrapers.etherscan_scraper import scrape_ethereum_node_count
from util.chrome_driver_manager import ChromeDriverManager
from util.date_gate import DateGate
from util.link_loader import LinkLoader


def get_price_num(price_str: str):
    return price_str.replace("$", "").replace(",", "")


def recreate_driver(driver):
    """Safely quit and recreate the Chrome driver."""
    try:
        driver.quit()
    except:
        pass
    return ChromeDriverManager.create_driver()


def run_scraper(label, scrape_fn, url, output_file, driver, transform=None):
    """
    Run a single scraper and save its result to a file.

    Args:
        label (str): Display name for logging.
        scrape_fn (callable): Scraper function to call.
        url (str): URL to pass to the scraper.
        output_file (str): Filename to write the result to.
        driver: Shared Chrome driver instance.
        transform (callable, optional): Transform applied to result before saving.

    Returns:
        tuple: (success: bool, value: str|None, driver: updated driver)
    """
    try:
        value = scrape_fn(url, driver)
        if value:
            print(f"✓ {label}: {value}")
            try:
                output = transform(value) if transform else value
                with open(output_file, "w") as f:
                    f.write(output)
                print(f"✓ Saved to {output_file}")
                return True, value, driver
            except Exception as e:
                print(f"✗ Error writing to {output_file}: {str(e)}")
                return False, value, driver
        else:
            print(f"✗ Failed to scrape {label}")
            return False, None, driver
    except Exception as e:
        print(f"✗ {label} scraper crashed: {str(e)}")
        print("Recreating web driver...")
        driver = recreate_driver(driver)
        return False, None, driver


def main():
    gate = DateGate()

    """Main function to run all enabled scrapers"""
    print("=" * 60)
    print("Starting Home Value and Node Count Scraper")
    print("=" * 60)

    if not gate.proceed():
        print("Already ran today. Skipping operation.")
        sys.exit(0)

    # Load links from configuration
    print("\nLoading links from configuration...")
    print("-" * 60)
    try:
        LinkLoader.load()
    except Exception as e:
        print(f"✗ Error loading links: {str(e)}")
        sys.exit(1)

    # Full scraper registry — url will be None if disabled in links.json
    scrapers = [
        ("Redfin",      scrape_redfin_home_value,        LinkLoader.redfin,     "redfin.txt",     get_price_num),
        ("Zillow",      scrape_zillow_zestimate,          LinkLoader.zillow,     "zillow.txt",     get_price_num),
        ("Realtor.com", scrape_realtor_home_value,        LinkLoader.realtor,    "realtor.txt",    get_price_num),
        ("Bitnodes",    scrape_bitcoin_node_count,        LinkLoader.bitnodes,   "bitnodes.txt",   get_price_num),
        ("Coin.dance",  scrape_coindance_node_count,      LinkLoader.coindance,  "coindance.txt",  get_price_num),
        ("Etherscan",   scrape_ethereum_node_count,       LinkLoader.etherscan,  "etherscan.txt",  get_price_num),
    ]

    enabled_scrapers = [(label, fn, url, out, tx) for label, fn, url, out, tx in scrapers if url is not None]
    total = len(enabled_scrapers)

    if total == 0:
        print("✗ No scrapers are enabled. Check links.json.")
        sys.exit(1)

    # Track results: label -> (success, value, output_file)
    results = {}

    # Create a single shared Chrome driver
    print("\nInitializing shared Chrome driver...")
    print("-" * 60)
    driver = ChromeDriverManager.create_driver()

    try:
        for i, (label, fn, url, output_file, transform) in enumerate(enabled_scrapers, start=1):
            print(f"\n[{i}/{total}] Scraping {label}...")
            print("-" * 60)
            success, value, driver = run_scraper(label, fn, url, output_file, driver, transform)
            results[label] = (success, value, output_file)

    finally:
        print("\nClosing shared Chrome driver...")
        try:
            driver.quit()
        except:
            pass

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    for label, fn, url, output_file, _ in scrapers:
        if url is None:
            print(f"{label + ':':<14} SKIPPED (disabled)")
        else:
            success, value, out = results[label]
            if success:
                print(f"{label + ':':<14} {value} → {out}")
            else:
                print(f"{label + ':':<14} FAILED")

    print("=" * 60)

    gate.save_date()

    # Exit based on enabled scrapers only
    successes = [s for s, _, __ in results.values()]
    if all(successes):
        print("\n✓ All enabled scrapers completed successfully!")
        sys.exit(0)
    elif any(successes):
        print("\n⚠ Some scrapers failed")
        sys.exit(1)
    else:
        print("\n✗ All scrapers failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
