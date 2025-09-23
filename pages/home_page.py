"""
Module: home_page.py
Defines the HomePage Tkinter frame showing total balance.
"""

import tkinter as tk

class HomePage(tk.Frame):
    """Home page frame displaying total balance and navigation buttons."""
    def __init__(self, parent, controller, savings_list, spendings_list):
        super().__init__(parent)
        self.controller = controller
        self.savings_list = savings_list
        self.spendings_list = spendings_list

        tk.Label(self, text="Home Page", font=("Arial", 18)).pack(pady=10)

        self.balance_label = tk.Label(self, text="Total Balance: $0", font=("Arial", 16))
        self.balance_label.pack(pady=20)

        tk.Button(self, text="Go to Savings", width=20, command=lambda: controller.show_frame("SavingsPage")).pack(pady=5)
        tk.Button(self, text="Go to Spendings", width=20, command=lambda: controller.show_frame("SpendingsPage")).pack(pady=5)
        tk.Button(self, text="Go to Goals", width=20, command=lambda: controller.show_frame("GoalsPage")).pack(pady=5)

    def update_balance(self):
        total_savings = sum([t.amount for t in self.savings_list])
        total_spendings = sum([t.amount for t in self.spendings_list])
        total = total_savings - total_spendings
        self.balance_label.config(text=f"Total Balance: ${total:.2f}")