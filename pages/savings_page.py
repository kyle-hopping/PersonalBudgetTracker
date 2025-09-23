"""
Module: savings_page.py
Defines the SavingsPage Tkinter frame for adding and listing savings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Transaction
from pages.base_page import BasePage
from styles import BODY_FONT, BUTTON_FONT, ENTRY_FONT, TREEVIEW_FONT

class SavingsPage(BasePage):
    """Page for adding and listing savings."""
    def __init__(self, parent, controller, savings_list):
        super().__init__(parent, controller, "Savings")
        self.savings_list = savings_list

        # Input frame
        input_frame = tk.Frame(self.content, bg="#f0f4f7")
        input_frame.pack(pady=10, fill="x")

        tk.Label(input_frame, text="Amount:", bg="#f0f4f7", font=BODY_FONT).pack(anchor="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=ENTRY_FONT)
        self.amount_entry.pack(fill="x", padx=5, pady=5)

        tk.Label(input_frame, text="Description:", bg="#f0f4f7", font=BODY_FONT).pack(anchor="w", padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, font=ENTRY_FONT)
        self.desc_entry.pack(fill="x", padx=5, pady=5)

        tk.Button(input_frame, text="Add Saving", bg="#4caf50", fg="white", font=BUTTON_FONT, command=self.add_saving).pack(pady=10, fill="x")

        # Treeview
        self.tree = ttk.Treeview(self.content, columns=("Amount", "Description"), show="headings", height=8)
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.pack(pady=10, fill="x")

        # Style for alternating row colors
        self.tree.tag_configure("oddrow", background="#ffe0b2", font=TREEVIEW_FONT)
        self.tree.tag_configure("evenrow", background="#ffffff", font=TREEVIEW_FONT)

        # Remove button
        tk.Button(self.content, text="Remove Selected", bg="#f44336", fg="white", font=BUTTON_FONT, command=self.remove_selected).pack(pady=5, fill="x")

        self.update_tree()

    def add_saving(self):
        """Add a saving transaction."""
        try:
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get()
            t = Transaction(amount, description)
            self.savings_list.append(t)
            self.update_tree()
            self.amount_entry.delete(0, "end")
            self.desc_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    def update_tree(self):
        """Refresh the treeview with current savings."""
        self.tree.delete(*self.tree.get_children())
        for i, t in enumerate(self.savings_list):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(t.amount, t.description), tags=(tag,))

    def remove_selected(self):
        """Remove the selected saving transaction."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No item selected")
            return
        for item in selected:
            index = self.tree.index(item)
            self.savings_list.pop(index)
        self.update_tree()