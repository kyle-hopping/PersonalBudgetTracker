import tkinter as tk
from styles import TITLE_FONT, BUTTON_FONT
from tkinter import ttk

class BasePage(tk.Frame):
    """Base page with top banner and bottom navigation bar"""
    def __init__(self, parent, controller, page_name):
        super().__init__(parent, bg="#f0f4f7")
        self.controller = controller

        # --- Top banner ---
        self.banner = tk.Frame(self, bg="#1a237e", height=60)
        self.banner.pack(fill="x")
        self.banner.pack_propagate(False)
        self.title_label = tk.Label(self.banner, text=page_name, font=(TITLE_FONT), bg="#1a237e", fg="white")
        self.title_label.pack(expand=True)

        # Content frame
        self.content = tk.Frame(self, bg="#f0f4f7")
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.content.pack_propagate(False)

        # Bottom navigation banner
        self.bottom_nav = tk.Frame(self, bg="#1a237e", height=60)
        self.bottom_nav.pack(fill="x", side="bottom")
        self.bottom_nav.pack_propagate(False)

        # Page navigation buttons
        btn_params = {"width": 20, "font": BUTTON_FONT,"bg": "#283593", "fg": "white", "bd": 0,"relief": "raised", "pady":5}

        tk.Button(self.bottom_nav, text="Home", command=lambda: controller.show_frame("HomePage"), **btn_params).pack(side="left", expand=True)
        tk.Button(self.bottom_nav, text="Savings", command=lambda: controller.show_frame("SavingsPage"), **btn_params).pack(side="left", expand=True)
        tk.Button(self.bottom_nav, text="Spendings", command=lambda: controller.show_frame("SpendingsPage"), **btn_params).pack(side="left", expand=True)
        tk.Button(self.bottom_nav, text="Goals", command=lambda: controller.show_frame("GoalsPage"), **btn_params).pack(side="left", expand=True)
