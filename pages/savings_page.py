"""
Module: savings_page.py
Defines the SavingsPage Tkinter frame for adding and listing savings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Transaction

class SavingsPage(tk.Frame):
    """Frame to manage savings transactions."""
    def __init__(self, parent, controller, savings_list):
        super().__init__(parent)
        self.controller = controller
        self.savings_list = savings_list

        tk.Label(self, text="Savings Page", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Amount:").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        tk.Label(self, text="Description:").pack()
        self.desc_entry = tk.Entry(self)
        self.desc_entry.pack()

        tk.Button(self, text="Add Saving", command=self.add_saving).pack(pady=5)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack(pady=5)

        # Treeview to display transactions
        self.tree = ttk.Treeview(self, columns=("Amount", "Description"), show="headings")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.pack(pady=10, fill="x")

        self.update_tree()

    def add_saving(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get()
            t = Transaction(amount, description)
            self.savings_list.append(t)
            self.update_tree()
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Saving added!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        for t in self.savings_list:
            self.tree.insert("", tk.END, values=(t.amount, t.description))