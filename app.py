"""
Module: app.py
Contains the main BudgetApp Tkinter controller.
"""

import tkinter as tk
from pages.home_page import HomePage
from pages.savings_page import SavingsPage
from pages.spendings_page import SpendingsPage
from pages.goals_page import GoalsPage
from utils import storage

class BudgetApp(tk.Tk):
    """Main application controller for Personal Budget Tracker."""
    def __init__(self):
        super().__init__()
        self.title("Personal Budget Tracker")
        self.geometry("600x400")

        # Load data
        self.savings_list, self.spendings_list, self.goals_list = storage.load_data()

        # Page frames
        self.frames = {}
        for Page in (HomePage, SavingsPage, SpendingsPage, GoalsPage):
            page_name = Page.__name__
            if Page == HomePage:
                frame = Page(self, self, self.savings_list, self.spendings_list)
            elif Page == SavingsPage:
                frame = Page(self, self, self.savings_list)
            elif Page == SpendingsPage:
                frame = Page(self, self, self.spendings_list)
            else:
                frame = Page(self, self, self.goals_list)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        # Save data on close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "HomePage":
            frame.update_balance()
        frame.tkraise()

    def on_close(self):
        """Save data and close the application."""
        storage.save_data(self.savings_list, self.spendings_list, self.goals_list)
        self.destroy()