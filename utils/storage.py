"""
Module: storage.py
Handles saving and loading of data (savings, spendings, goals) in JSON format.
"""

import json
from models.transaction import Transaction
from models.goal import Goal

DATA_FILE = "budget_data.json"

def save_data(savings, spendings, goals):
    """Save all data to a JSON file."""
    data = {
        "savings": [{"amount": t.amount, "description": t.description} for t in savings],
        "spendings": [{"amount": t.amount, "description": t.description} for t in spendings],
        "goals": [g.to_dict() for g in goals]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    """Load data from JSON file. Returns savings, spendings, goals."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        savings = [Transaction(t["amount"], t["description"]) for t in data.get("savings", [])]
        spendings = [Transaction(t["amount"], t["description"]) for t in data.get("spendings", [])]
        goals = [Goal.from_dict(g) for g in data.get("goals", [])]
        return savings, spendings, goals
    except FileNotFoundError:
        return [], [], []