"""
Module: goal.py
Defines the Goal class for savings targets.
"""

class Goal:
    """Represents a financial goal with a target amount."""
    def __init__(self, name: str, target_amount: float, saved_amount: float = 0):
        self.name = name
        self.target_amount = target_amount
        self.saved_amount = saved_amount

    def progress_percentage(self) -> float:
        """Return the percentage of the goal achieved."""
        if self.target_amount == 0:
            return 0
        return min(100, (self.saved_amount / self.target_amount) * 100)

    def to_dict(self) -> dict:
        """Convert Goal to dictionary for JSON storage."""
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "saved_amount": self.saved_amount
        }

    @staticmethod
    def from_dict(data: dict):
        """Create Goal object from dictionary."""
        return Goal(
            name=data["name"],
            target_amount=data["target_amount"],
            saved_amount=data.get("saved_amount", 0)
        )