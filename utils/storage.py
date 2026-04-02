# utils/storage.py
# Load and save budget data to a local JSON file.

import json
import os
from styles import DEFAULT_ALLOCATIONS

DATA_FILE = "budget_data.json"

def load_data() -> dict:
    # Load data from JSON file, returning defaults if file is missing or corrupt.
    if not os.path.exists(DATA_FILE):
        return _default_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return _default_data()

def save_data(data: dict) -> None:
    # Persist data dict to JSON file.
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except IOError as exc:
        print(f"[BudgetTracker] Failed to save data: {exc}")

def _default_data() -> dict:
    return {
        "income": 0.0,
        "expenses": [],
        "savings_allocations": DEFAULT_ALLOCATIONS,
        "goals": [],
    }
