"""
Module: goals_page.py
Defines GoalsPage frame for creating and tracking financial goals.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.goal import Goal

class GoalsPage(tk.Frame):
    """Frame for managing financial goals."""
    def __init__(self, parent, controller, goals_list=None):
        super().__init__(parent)
        self.controller = controller
        self.goals_list = goals_list if goals_list is not None else []

        tk.Label(self, text="Goals Page", font=("Arial", 18)).pack(pady=10)

        # Entry for new goal
        tk.Label(self, text="Goal Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Target Amount:").pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        tk.Button(self, text="Add Goal", command=self.add_goal).pack(pady=5)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage")).pack(pady=5)

        # Treeview to show goals with progress
        self.tree = ttk.Treeview(self, columns=("Goal", "Target", "Saved", "Progress"), show="headings")
        self.tree.heading("Goal", text="Goal")
        self.tree.heading("Target", text="Target")
        self.tree.heading("Saved", text="Saved")
        self.tree.heading("Progress", text="Progress (%)")
        self.tree.pack(pady=10, fill="x")

        self.update_tree()

    def add_goal(self):
        name = self.name_entry.get()
        try:
            target = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for target amount")
            return

        if not name:
            messagebox.showerror("Error", "Enter a goal name")
            return

        goal = Goal(name, target)
        self.goals_list.append(goal)
        self.update_tree()
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Goal added!")

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        for g in self.goals_list:
            self.tree.insert("", tk.END, values=(g.name, g.target_amount, g.saved_amount, f"{g.progress_percentage():.1f}%"))
