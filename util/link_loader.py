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
    
    Each entry in the config is expected to have the shape:
        { "link": "https://...", "enabled": true }
    """
    
    # Public class variables for scraper URLs (None if disabled or not loaded)
    redfin = None
    zillow = None
    realtor = None
    bitnodes = None
    coindance = None
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
        
        # Load each URL from the config; set to None if disabled
        cls.redfin    = links['redfin']['link']    if links['redfin']['enabled']    else None
        cls.zillow    = links['zillow']['link']    if links['zillow']['enabled']    else None
        cls.realtor   = links['realtor']['link']   if links['realtor']['enabled']   else None
        cls.bitnodes  = links['bitnodes']['link']  if links['bitnodes']['enabled']  else None
        cls.coindance = links['coindance']['link'] if links['coindance']['enabled'] else None
        cls.etherscan = links['etherscan']['link'] if links['etherscan']['enabled'] else None
        
        print(f"Successfully loaded links from {config_file}")
    
    @classmethod
    def get_all(cls):
        """
        Get all loaded URLs as a dictionary.
        
        Returns:
            dict: Dictionary containing all scraper URLs (None if disabled).
        """
        return {
            'redfin':    cls.redfin,
            'zillow':    cls.zillow,
            'realtor':   cls.realtor,
            'bitnodes':  cls.bitnodes,
            'coindance': cls.coindance,
            'etherscan': cls.etherscan,
        }
    
    @classmethod
    def is_loaded(cls):
        """
        Check if all enabled links have been loaded.
        
        Returns:
            bool: True if all links are loaded (enabled ones are non-None).
        """
        return all([
            cls.redfin is not None,
            cls.zillow is not None,
            cls.realtor is not None,
            cls.bitnodes is not None,
            cls.coindance is not None,
            cls.etherscan is not None,
        ])
