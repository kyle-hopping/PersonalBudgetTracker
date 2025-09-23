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

        # Window settings
        window_width = 1200
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

        # Load data
        self.savings_list, self.spendings_list, self.goals_list = storage.load_data()

        self.frames = {}
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for Page in (HomePage, SavingsPage, SpendingsPage, GoalsPage):
            page_name = Page.__name__
            if Page == HomePage:
                frame = Page(container, self, self.savings_list, self.spendings_list)
            elif Page == SavingsPage:
                frame = Page(container, self, self.savings_list)
            elif Page == SpendingsPage:
                frame = Page(container, self, self.spendings_list)
            else:
                frame = Page(container, self, self.goals_list)

            self.frames[page_name] = frame
            frame.pack(fill="both", expand=True)

        # Show the initial page
        self.show_frame("HomePage")

        # Save data on close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_frame(self, page_name):
        """Raise the specified page to the front."""
        for name, frame in self.frames.items():
            frame.pack_forget()
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        if page_name == "HomePage":
            frame.update_balance()

    def on_close(self):
        """Save data and close the application."""
        storage.save_data(self.savings_list, self.spendings_list, self.goals_list)
        self.destroy()