#!/usr/bin/env python3
"""
Link Loader
Loads and provides access to scraper URLs from a JSON configuration file
"""

import json
from pathlib import Path


class LinkLoader:
    """
    A class that loads and stores URLs for various scrapers.
    
    Links are loaded from a JSON configuration file and exposed as
    public class variables accessible by all scrapers.
    """
    
    # Public class variables for scraper URLs
    redfin = None
    zillow = None
    realtor = None
    bitnodes = None
    etherscan = None
    
    @classmethod
    def load(cls, config_file="links.json"):
        """
        Load URLs from a JSON configuration file.
        
        Args:
            config_file: Path to the JSON config file. Defaults to "links.json".
            
        Raises:
            FileNotFoundError: If the config file doesn't exist.
            json.JSONDecodeError: If the config file is not valid JSON.
            KeyError: If required keys are missing from the config.
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file '{config_file}' not found")
        
        with open(config_path, 'r') as f:
            links = json.load(f)
        
        # Load each URL from the config
        cls.redfin = links['redfin']
        cls.zillow = links['zillow']
        cls.realtor = links['realtor']
        cls.bitnodes = links['bitnodes']
        cls.etherscan = links['etherscan']
        
        print(f"Successfully loaded links from {config_file}")
    
    @classmethod
    def get_all(cls):
        """
        Get all loaded URLs as a dictionary.
        
        Returns:
            dict: Dictionary containing all scraper URLs.
        """
        return {
            'redfin': cls.redfin,
            'zillow': cls.zillow,
            'realtor': cls.realtor,
            'bitnodes': cls.bitnodes,
            'etherscan': cls.etherscan
        }
    
    @classmethod
    def is_loaded(cls):
        """
        Check if links have been loaded.
        
        Returns:
            bool: True if all links are loaded, False otherwise.
        """
        return all([
            cls.redfin is not None,
            cls.zillow is not None,
            cls.realtor is not None,
            cls.bitnodes is not None,
            cls.etherscan is not None
        ])
