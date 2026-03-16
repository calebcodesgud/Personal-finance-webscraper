#!/usr/bin/env python3
"""
Chrome Driver Manager
Provides a reusable ChromeDriver instance for web scraping
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import platform


class ChromeDriverManager:
    """Manages Chrome WebDriver instances for web scraping"""

    @staticmethod
    def _is_kubuntu() -> bool:
        """Return True if running on Kubuntu by checking /etc/os-release"""
        try:
            with open("/etc/os-release") as f:
                contents = f.read().lower()
            return "ubuntu" in contents
        except OSError:
            return False

    @staticmethod
    def create_driver():
        """
        Create and return a Chrome WebDriver instance

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver instance
        """
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Detect OS and set appropriate user agent
        system = platform.system()
        if system == "Windows":
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        elif system == "Linux":
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        elif system == "Darwin":  # macOS
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        else:
            user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        chrome_options.add_argument(f"user-agent={user_agent}")

        # Initialize the Chrome driver
        # Supply explicit service only on Kubuntu (not CachyOS or other distros)
        if system == "Linux" and ChromeDriverManager._is_kubuntu():
            CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
            service = Service(executable_path=CHROME_DRIVER_PATH)
            service.log_path = "/tmp/chromedriver_shared.log"
            print(f"Kubuntu detected — starting Chrome with chromedriver at: {CHROME_DRIVER_PATH}")
            driver = webdriver.Chrome(options=chrome_options, service=service)
        else:
            driver = webdriver.Chrome(options=chrome_options)

        print("Chrome driver started successfully")
        return driver
