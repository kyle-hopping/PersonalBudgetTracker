# app.py
# Root Tkinter window. Builds the sidebar and swaps page frames.

import tkinter as tk
from models.budget_model import BudgetModel
from pages.home_page     import HomePage
from pages.expenses_page import ExpensesPage
from pages.savings_page  import SavingsPage
from pages.goals_page    import GoalsPage
from styles import COLORS, FONTS

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Budget Tracker")
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)
        self.minsize(960, 640)
        self._center(1240, 780)

        self.model = BudgetModel()

        self._build_sidebar()
        self._build_content()
        self._build_pages()

        self.show_page("home")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ----- Helpers -----
    def _center(self, w: int, h: int):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    # ----- Layout -----
    def _build_sidebar(self):
        self._sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=215)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # App logo / title block
        title_blk = tk.Frame(self._sidebar, bg=COLORS["primary_dark"], height=72)
        title_blk.pack(fill="x")
        title_blk.pack_propagate(False)
        tk.Label(title_blk, text="BudgetPro", font=FONTS["app_title"],
                 bg=COLORS["primary_dark"], fg="white").pack(expand=True)

        tk.Frame(self._sidebar, bg=COLORS["primary_dark"], height=2).pack(fill="x")
        tk.Frame(self._sidebar, bg=COLORS["sidebar"], height=18).pack()

        # Section label
        tk.Label(self._sidebar, text="NAVIGATION", font=("Helvetica", 8, "bold"),
                 bg=COLORS["sidebar"], fg="#4a8a6a",
                 anchor="w", padx=22).pack(fill="x", pady=(0, 6))

        self._nav_btns: dict = {}
        nav = [
            ("home", "🏠", "Dashboard"),
            ("expenses", "💳", "Expenses"),
            ("savings", "💵", "Savings"),
            ("goals", "🎯", "Goals"),
        ]
        for key, icon, label in nav:
            btn = tk.Button(
                self._sidebar,
                text=f"  {icon}  {label}",
                font=FONTS["sidebar_item"],
                bg=COLORS["sidebar"], fg="black",
                bd=0, pady=13, padx=14, anchor="w",
                cursor="hand2",
                activebackground=COLORS["sidebar_hover"],
                activeforeground="black",
                command=lambda k=key: self.show_page(k),
            )
            btn.pack(fill="x")
            self._nav_btns[key] = btn

        # Bottom version badge
        tk.Label(self._sidebar, text="v2.0", font=FONTS["small"],
                 bg=COLORS["sidebar"], fg="#3a7a5a").pack(side="bottom", pady=12)

    def _build_content(self):
        self._content = tk.Frame(self, bg=COLORS["bg"])
        self._content.pack(side="left", fill="both", expand=True)

    def _build_pages(self):
        # Create page frames and stack them using `place` so we can
        # lift the desired page to the front without re-packing.
        self._pages: dict = {
            "home":     HomePage(self._content, self),
            "expenses": ExpensesPage(self._content, self),
            "savings":  SavingsPage(self._content, self),
            "goals":    GoalsPage(self._content, self),
        }
        for p in self._pages.values():
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

    # ----- Navigation -----
    def show_page(self, name: str):
        # Update nav button highlights
        for key, btn in self._nav_btns.items():
            active = key == name
            btn.configure(
                bg=COLORS["sidebar_hover"] if active else COLORS["sidebar"],
                font=FONTS["nav_active"] if active else FONTS["sidebar_item"],
            )

        # Bring the requested page to front (no re-packing).
        page = self._pages[name]
        page.lift()

        # Call refresh if the page implements it.
        if hasattr(page, "refresh"):
            page.refresh()

    # ----- Close -----
    def _on_close(self):
        self.model.save()
        self.destroy()
