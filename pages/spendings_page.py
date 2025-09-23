"""
Module: spendings_page.py
Defines the SpendingsPage frame for adding and listing spendings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Transaction

class SpendingsPage(tk.Frame):
    """Frame to manage spending transactions."""
    def __init__(self, parent, controller, spendings_list):
        super().__init__(parent)
        self.controller = controller
        self.spendings_list = spendings_list

        tk.Label(self, text="Spendings Page", font=("Arial", 18)).pack(pady=10)

        # Entry fields for new spending
        tk.Label(self, text="Amount:").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        tk.Label(self, text="Description:").pack()
        self.desc_entry = tk.Entry(self)
        self.desc_entry.pack()

        # Buttons
        tk.Button(self, text="Add Spending", command=self.add_spending).pack(pady=5)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack(pady=5)

        # Treeview to display all spendings
        self.tree = ttk.Treeview(self, columns=("Amount", "Description"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.pack(pady=10, fill="x")

        self.update_tree()

    def add_spending(self):
        """Add a spending transaction to the list."""
        try:
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get()
            t = Transaction(amount, description)
            self.spendings_list.append(t)
            self.update_tree()
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Spending added!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def update_tree(self):
        """Update the Treeview with the current spendings list."""
        self.tree.delete(*self.tree.get_children())
        for t in self.spendings_list:
            self.tree.insert("", tk.END, values=(t.amount, t.description))
