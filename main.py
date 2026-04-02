# Entry point for the application

import matplotlib
matplotlib.use("TkAgg")

from app import BudgetApp

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()