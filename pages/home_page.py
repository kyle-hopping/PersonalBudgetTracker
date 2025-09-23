"""
Module: home_page.py
Defines the HomePage Tkinter frame showing total balance.
"""

import tkinter as tk
from pages.base_page import BasePage
from styles import BODY_FONT

class HomePage(BasePage):
    """Home page showing total balance and summaries."""
    def __init__(self, parent, controller, savings_list, spendings_list):
        super().__init__(parent, controller, "Home")
        self.savings_list = savings_list
        self.spendings_list = spendings_list

        # Total balance
        self.balance_label = tk.Label(self.content, text="Total Balance: $0", font=BODY_FONT, bg="#f0f4f7")
        self.balance_label.pack(pady=(40, 20))  # more top padding

        # Summary frames
        summary_frame = tk.Frame(self.content, bg="#f0f4f7")
        summary_frame.pack(pady=10, fill="x")

        self.savings_summary = tk.Label(summary_frame, text="Total Savings: $0", font=("Helvetica", 14), bg="#c8e6c9", fg="#256029", pady=10)
        self.savings_summary.pack(fill="x", pady=5)

        self.spendings_summary = tk.Label(summary_frame, text="Total Spendings: $0", font=("Helvetica", 14), bg="#ffcdd2", fg="#b71c1c", pady=10)
        self.spendings_summary.pack(fill="x", pady=5)

    def update_balance(self):
        """Update the total balance and summary labels."""
        total_savings = sum([t.amount for t in self.savings_list])
        total_spendings = sum([t.amount for t in self.spendings_list])
        total = total_savings - total_spendings

        self.balance_label.config(text=f"Total Balance: ${total:.2f}")
        self.savings_summary.config(text=f"Total Savings: ${total_savings:.2f}")
        self.spendings_summary.config(text=f"Total Spendings: ${total_spendings:.2f}")