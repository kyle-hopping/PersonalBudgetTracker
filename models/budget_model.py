# models/budget_model.py
# Central data model for income, expenses, savings, and goals.
# All mutations call save() automatically so the UI never needs to manage persistence.

from utils.storage import load_data, save_data

class BudgetModel:
    def __init__(self):
        self._data = load_data()

    # ----- Income -----
    @property
    def income(self) -> float:
        return float(self._data.get("income", 0.0))

    @income.setter
    def income(self, value: float):
        self._data["income"] = float(value)
        self.save()

    # ----- Expenses -----
    @property
    def expenses(self) -> list:
        return list(self._data.get("expenses", []))

    @property
    def total_expenses(self) -> float:
        return sum(float(e.get("amount", 0)) for e in self._data.get("expenses", []))

    @property
    def total_savings(self) -> float:
        return max(0.0, self.income - self.total_expenses)

    def add_expense(self, description: str, category: str,
                    amount: float, date: str = "") -> dict:
        expense = {
            "id":          self._next_id("expenses"),
            "description": description,
            "category":    category,
            "amount":      float(amount),
            "date":        date,
        }
        self._data.setdefault("expenses", []).append(expense)
        self.save()
        return expense

    def update_expense(self, expense_id: int, **kwargs):
        for exp in self._data.get("expenses", []):
            if exp["id"] == expense_id:
                for key, val in kwargs.items():
                    exp[key] = float(val) if key == "amount" else val
                break
        self.save()

    def delete_expense(self, expense_id: int):
        self._data["expenses"] = [
            e for e in self._data.get("expenses", []) if e["id"] != expense_id
        ]
        self.save()

    def expenses_by_category(self) -> dict:
        """Return {category: total_amount} for all expenses."""
        totals: dict = {}
        for e in self._data.get("expenses", []):
            cat = e.get("category", "Other")
            totals[cat] = totals.get(cat, 0.0) + float(e.get("amount", 0))
        return totals

    # ----- Savings Allocations -----
    @property
    def savings_allocations(self) -> list:
        return list(self._data.get("savings_allocations", []))

    def update_savings_allocations(self, allocations: list):
        self._data["savings_allocations"] = allocations
        self.save()

    # ----- Goals -----
    @property
    def goals(self) -> list:
        return list(self._data.get("goals", []))

    def add_goal(self, name: str, target: float,
                 current: float = 0.0, color: str = "#4895ef") -> dict:
        goal = {
            "id":      self._next_id("goals"),
            "name":    name,
            "target":  float(target),
            "current": float(current),
            "color":   color,
        }
        self._data.setdefault("goals", []).append(goal)
        self.save()
        return goal

    def update_goal(self, goal_id: int, **kwargs):
        for goal in self._data.get("goals", []):
            if goal["id"] == goal_id:
                for key, val in kwargs.items():
                    goal[key] = float(val) if key in ("target", "current") else val
                break
        self.save()

    def delete_goal(self, goal_id: int):
        self._data["goals"] = [
            g for g in self._data.get("goals", []) if g["id"] != goal_id
        ]
        self.save()

    # ----- Helpers -----
    def _next_id(self, key: str) -> int:
        items = self._data.get(key, [])
        return max((item["id"] for item in items), default=0) + 1

    def save(self):
        save_data(self._data)
