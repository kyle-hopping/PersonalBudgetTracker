"""
Module: goals_page.py
Defines GoalsPage frame for creating and tracking financial goals.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.goal import Goal
from pages.base_page import BasePage
from styles import BODY_FONT, BUTTON_FONT, ENTRY_FONT

class GoalsPage(BasePage):
    """Page for creating and tracking financial goals."""
    def __init__(self, parent, controller, goals_list):
        super().__init__(parent, controller, "Goals")
        self.goals_list = goals_list

        # Input frame
        input_frame = tk.Frame(self.content, bg="#f0f4f7")
        input_frame.pack(pady=10, fill="x")

        tk.Label(input_frame, text="Goal Name:", bg="#f0f4f7", font=BODY_FONT).pack(anchor="w", padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, font=ENTRY_FONT)
        self.name_entry.pack(fill="x", padx=5, pady=5)

        tk.Label(input_frame, text="Target Amount:", bg="#f0f4f7", font=BODY_FONT).pack(anchor="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, font=ENTRY_FONT)
        self.amount_entry.pack(fill="x", padx=5, pady=5)

        tk.Button(input_frame, text="Add Goal", bg="#2196f3", fg="white", font=BUTTON_FONT, command=self.add_goal).pack(pady=10, fill="x")

        # Treeview with progress
        self.tree = ttk.Treeview(self.content, columns=("Goal", "Target", "Saved", "Progress"), show="headings", height=8)
        self.tree.heading("Goal", text="Goal")
        self.tree.heading("Target", text="Target")
        self.tree.heading("Saved", text="Saved")
        self.tree.heading("Progress", text="Progress (%)")
        self.tree.pack(pady=10, fill="x")

        # Remove button
        tk.Button(self.content, text="Remove Selected", bg="#f44336", fg="white", font=BUTTON_FONT,command=self.remove_selected).pack(pady=5, fill="x")

        self.update_tree()

    def add_goal(self):
        """Add a new goal to the list."""
        name = self.name_entry.get()
        try:
            target = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for target")
            return
        if not name.strip():
            messagebox.showerror("Error", "Enter a goal name")
            return

        goal = Goal(name, target)
        self.goals_list.append(goal)
        self.update_tree()
        self.name_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")

    def update_tree(self):
        """Refresh the treeview with current goals."""
        self.tree.delete(*self.tree.get_children())
        for g in self.goals_list:
            self.tree.insert("", "end", values=(g.name, f"${g.target_amount:.2f}", f"${g.saved_amount:.2f}", f"{g.progress_percentage():.1f}%"))
    
    def remove_selected(self):
        """Remove the selected spending transaction."""
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Warning", "No item selected")
            return
        for item in selected:
            index = self.tree.index(item)
            self.goals_list.pop(index)
        self.update_tree()
