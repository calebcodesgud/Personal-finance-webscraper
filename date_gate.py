#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path

class DateGate:
    """
    A class that manages date-based gating functionality.

    Tracks the last successful date and determines whether to proceed
    based on whether the current date differs from the saved date.
    """

    def __init__(self, filepath="last_success"):
        """
        Initialize the DateGate.

        Args:
            filepath: Path to the file where the last success date is stored.
                        Defaults to "last_success".
        """
        self.filepath = Path(filepath)

    def save_date(self):
        """
        Write the current date to the file.

        Saves the current date in YYYY-MM-DD format to the configured file.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.filepath.write_text(current_date)

    def proceed(self):
        """
        Check if the current date is different from the saved date.

        Returns:
            bool: True if the saved date is different from the current date
                    or if no date has been saved yet, False otherwise.
        """
        current_date = datetime.now().strftime("%Y-%m-%d")

        # If file doesn't exist, proceed (first run)
        if not self.filepath.exists():
            return True

        # Read the saved date
        saved_date = self.filepath.read_text().strip()

        # Return True if dates are different
        return saved_date != current_date
