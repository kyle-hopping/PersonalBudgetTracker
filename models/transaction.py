"""
Module: transaction.py
Defines the Transaction class used for savings and spendings.
"""

class Transaction:
    """Represents a single financial transaction."""
    def __init__(self, amount: float, description: str):
        self.amount = amount
        self.description = description