#!/usr/bin/env python3
"""
Combined Home Value and Node Count Scraper
Runs Redfin, Zillow, Realtor.com, Bitnodes, and Etherscan scrapers
"""

import sys
from scrapers.redfin_scraper import scrape_redfin_home_value
from scrapers.zillow_scraper import scrape_zillow_zestimate
from scrapers.realtor_scraper import scrape_realtor_home_value
from scrapers.bitnodes_scraper import scrape_bitcoin_node_count
from scrapers.etherscan_scraper import scrape_ethereum_node_count
from util.chrome_driver_manager import ChromeDriverManager
from util.date_gate import DateGate
from util.link_loader import LinkLoader


def get_price_num(price_str: str):
    return price_str.replace("$", "").replace(",", "")

def main():

    gate = DateGate()

    """Main function to run all scrapers"""
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

    # Track results
    redfin_success = False
    zillow_success = False
    realtor_success = False
    bitnodes_success = False
    etherscan_success = False

    # Create a single Chrome driver instance to be shared by all scrapers
    print("\nInitializing shared Chrome driver...")
    print("-" * 60)
    driver = ChromeDriverManager.create_driver()

    try:

        # Scrape Redfin
        print("\n[1/5] Scraping Redfin...")
        print("-" * 60)
        try:
            redfin_value = scrape_redfin_home_value(LinkLoader.redfin, driver)

            if redfin_value:
                print(f"✓ Redfin value: {redfin_value}")
                try:
                    with open("redfin.txt", "w") as f:
                        f.write(get_price_num(redfin_value))
                    print("✓ Saved to redfin.txt")
                    redfin_success = True
                except Exception as e:
                    print(f"✗ Error writing to redfin.txt: {str(e)}")
            else:
                print("✗ Failed to scrape Redfin")
        except Exception as e:
            print(f"✗ Redfin scraper crashed: {str(e)}")
            print("Recreating web driver...")
            try:
                driver.quit()
            except:
                pass
            driver = ChromeDriverManager.create_driver()

        # Scrape Zillow
        print("\n[2/5] Scraping Zillow...")
        print("-" * 60)
        try:
            zillow_value = scrape_zillow_zestimate(LinkLoader.zillow, driver)

            if zillow_value:
                print(f"✓ Zillow Zestimate: {zillow_value}")
                try:
                    with open("zillow.txt", "w") as f:
                        f.write(get_price_num(zillow_value))
                    print("✓ Saved to zillow.txt")
                    zillow_success = True
                except Exception as e:
                    print(f"✗ Error writing to zillow.txt: {str(e)}")
            else:
                print("✗ Failed to scrape Zillow")
        except Exception as e:
            print(f"✗ Zillow scraper crashed: {str(e)}")
            print("Recreating web driver...")
            try:
                driver.quit()
            except:
                pass
            driver = ChromeDriverManager.create_driver()

        # Scrape Realtor.com
        print("\n[3/5] Scraping Realtor.com...")
        print("-" * 60)
        try:
            realtor_value = scrape_realtor_home_value(LinkLoader.realtor, driver)

            if realtor_value:
                print(f"✓ Realtor.com estimate: {realtor_value}")
                try:
                    with open("realtor.txt", "w") as f:
                        f.write(get_price_num(realtor_value))
                    print("✓ Saved to realtor.txt")
                    realtor_success = True
                except Exception as e:
                    print(f"✗ Error writing to realtor.txt: {str(e)}")
            else:
                print("✗ Failed to scrape Realtor.com")
        except Exception as e:
            print(f"✗ Realtor scraper crashed: {str(e)}")
            print("Recreating web driver...")
            try:
                driver.quit()
            except:
                pass
            driver = ChromeDriverManager.create_driver()

        # Scrape Bitnodes
        print("\n[4/5] Scraping Bitnodes...")
        print("-" * 60)
        try:
            bitnodes_value = scrape_bitcoin_node_count(LinkLoader.bitnodes, driver)

            if bitnodes_value:
                print(f"✓ Bitcoin nodes: {bitnodes_value}")
                try:
                    with open("bitnodes.txt", "w") as f:
                        f.write(get_price_num(bitnodes_value))
                    print("✓ Saved to bitnodes.txt")
                    bitnodes_success = True
                except Exception as e:
                    print(f"✗ Error writing to bitnodes.txt: {str(e)}")
            else:
                print("✗ Failed to scrape Bitnodes")
        except Exception as e:
            print(f"✗ Bitnodes scraper crashed: {str(e)}")
            print("Recreating web driver...")
            try:
                driver.quit()
            except:
                pass
            driver = ChromeDriverManager.create_driver()

        # Scrape Etherscan
        print("\n[5/5] Scraping Etherscan...")
        print("-" * 60)
        try:
            etherscan_value = scrape_ethereum_node_count(LinkLoader.etherscan, driver)

            if etherscan_value:
                print(f"✓ Ethereum nodes: {etherscan_value}")
                try:
                    with open("etherscan.txt", "w") as f:
                        f.write(get_price_num(etherscan_value))
                    print("✓ Saved to etherscan.txt")
                    etherscan_success = True
                except Exception as e:
                    print(f"✗ Error writing to etherscan.txt: {str(e)}")
            else:
                print("✗ Failed to scrape Etherscan")
        except Exception as e:
            print(f"✗ Etherscan scraper crashed: {str(e)}")

    finally:
        # Close the shared Chrome driver
        print("\nClosing shared Chrome driver...")
        if driver:
            try:
                driver.quit()
            except:
                pass

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    if redfin_success:
        print(f"Redfin:      {redfin_value} → redfin.txt")
    else:
        print("Redfin:      FAILED")

    if zillow_success:
        print(f"Zillow:      {zillow_value} → zillow.txt")
    else:
        print("Zillow:      FAILED")

    if realtor_success:
        print(f"Realtor.com: {realtor_value} → realtor.txt")
    else:
        print("Realtor.com: FAILED")

    if bitnodes_success:
        print(f"Bitnodes:    {bitnodes_value} → bitnodes.txt")
    else:
        print("Bitnodes:    FAILED")

    if etherscan_success:
        print(f"Etherscan:   {etherscan_value} → etherscan.txt")
    else:
        print("Etherscan:   FAILED")

    print("=" * 60)

    gate.save_date()

    # Exit with appropriate code
    if redfin_success and zillow_success and realtor_success and bitnodes_success and etherscan_success:
        print("\n✓ All scrapers completed successfully!")
        sys.exit(0)
    elif redfin_success or zillow_success or realtor_success or bitnodes_success or etherscan_success:
        print("\n⚠ Some scrapers failed")
        sys.exit(1)
    else:
        print("\n✗ All scrapers failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
