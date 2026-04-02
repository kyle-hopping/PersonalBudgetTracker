# pages/goals_page.py
# Financial goals with progress bars, add funds, edit, and delete.

import itertools
import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONTS, GOAL_COLORS

class GoalsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._color_cycle = itertools.cycle(GOAL_COLORS)
        self._build()

    # ----- Build -----
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=32, pady=(24, 14))
        tk.Label(hdr, text="Financial Goals", font=FONTS["heading"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        tk.Button(hdr, text="+ New Goal", font=FONTS["button"], bg=COLORS["primary"],
                  fg="black", relief="flat", padx=16, pady=8, cursor="hand2",
                  activebackground=COLORS["primary_dark"], activeforeground="black",
                  command=self._open_add).pack(side="right")

        # Stats strip
        strip = tk.Frame(self, bg=COLORS["bg"])
        strip.pack(fill="x", padx=32, pady=(0, 16))
        self._stats_lbl = tk.Label(strip, text="", font=FONTS["body"],
                                    bg=COLORS["bg"], fg=COLORS["text_muted"])
        self._stats_lbl.pack(side="left")

        # Scrollable goal cards area
        wrap = tk.Frame(self, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=(0, 22))

        canvas = tk.Canvas(wrap, bg=COLORS["bg"], highlightthickness=0)
        vsb = tk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
        self._goals_frame = tk.Frame(canvas, bg=COLORS["bg"])
        self._goals_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._goals_frame, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.bind("<Enter>",
            lambda _: canvas.bind_all("<MouseWheel>",
                lambda e, c=canvas: c.yview_scroll(-1*(e.delta//120), "units")))
        canvas.bind("<Leave>",
            lambda _: canvas.unbind_all("<MouseWheel>"))

    # ----- Refresh -----

    def refresh(self):
        for w in self._goals_frame.winfo_children():
            w.destroy()
        goals = self.app.model.goals

        # Stats
        if goals:
            completed = sum(1 for g in goals
                            if g.get("current", 0) >= g.get("target", 1))
            self._stats_lbl.config(
                text=f"{len(goals)} goals  ·  {completed} completed")
        else:
            self._stats_lbl.config(text="")

        if not goals:
            tk.Label(self._goals_frame,
                     text="No goals yet.  Click '+ New Goal' to set your first one!",
                     font=FONTS["body"], bg=COLORS["bg"],
                     fg=COLORS["text_muted"], pady=50).pack()
            return

        # 2-column card grid
        for i, goal in enumerate(goals):
            row_idx, col_idx = divmod(i, 2)
            card = self._goal_card(goal)
            card.grid(row=row_idx, column=col_idx,
                      padx=10, pady=10, sticky="nsew")

        self._goals_frame.columnconfigure(0, weight=1)
        self._goals_frame.columnconfigure(1, weight=1)

    # ----- Card -----

    def _goal_card(self, goal: dict) -> tk.Frame:
        color   = goal.get("color", COLORS["accent"])
        name    = goal.get("name", "Goal")
        current = float(goal.get("current", 0))
        target  = float(goal.get("target", 1))
        pct     = min(100.0, (current / target * 100) if target > 0 else 0)
        done    = current >= target

        card = tk.Frame(self._goals_frame, bg=COLORS["card"],
                        highlightbackground=COLORS["border"], highlightthickness=1)

        # Color accent bar
        tk.Frame(card, bg=color, height=7).pack(fill="x")

        body = tk.Frame(card, bg=COLORS["card"])
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # Name row + delete button
        name_row = tk.Frame(body, bg=COLORS["card"])
        name_row.pack(fill="x")
        tk.Label(name_row, text=("✓  " if done else "") + name,
                 font=FONTS["subheading"], bg=COLORS["card"],
                 fg=COLORS["success"] if done else COLORS["text"],
                 anchor="w").pack(side="left")
        tk.Button(name_row, text="✕", font=FONTS["small_bold"],
                  bg=COLORS["card"], fg=COLORS["danger"], relief="flat",
                  cursor="hand2", padx=4,
                  command=lambda gid=goal["id"]: self._delete(gid)).pack(side="right")

        # Amount display
        amt_row = tk.Frame(body, bg=COLORS["card"])
        amt_row.pack(fill="x", pady=(10, 4))
        tk.Label(amt_row, text=f"${current:,.2f}", font=FONTS["card_value"],
                 bg=COLORS["card"], fg=color).pack(side="left")
        tk.Label(amt_row, text=f" of ${target:,.2f}", font=FONTS["body"],
                 bg=COLORS["card"], fg=COLORS["text_muted"]).pack(side="left", pady=6)

        # Progress bar
        bar_outer = tk.Frame(body, bg=COLORS["border"], height=18)
        bar_outer.pack(fill="x", pady=(2, 4))
        bar_outer.pack_propagate(False)
        tk.Frame(bar_outer, bg=color,
                 height=18).place(relwidth=max(0.015, pct / 100), relheight=1)

        # Percentage text
        tk.Label(body, text=f"{pct:.1f}% complete",
                 font=FONTS["small"], bg=COLORS["card"],
                 fg=COLORS["success"] if done else COLORS["text_muted"],
                 anchor="w").pack(fill="x", pady=(0, 12))

        # Buttons
        btns = tk.Frame(body, bg=COLORS["card"])
        btns.pack(fill="x")

        if not done:
            tk.Button(btns, text="➕  Add Funds", font=FONTS["small_bold"],
                      bg=COLORS["primary"], fg="black", relief="flat", padx=10,
                      pady=5, cursor="hand2", activebackground=COLORS["primary_dark"],
                      activeforeground="black",
                      command=lambda g=goal: self._add_funds(g)).pack(
                          side="left", padx=(0, 6))

        tk.Button(btns, text="✎  Edit", font=FONTS["small_bold"],
                  bg=COLORS["accent"], fg="black", relief="flat", padx=10,
                  pady=5, cursor="hand2", activebackground=COLORS["accent_dark"],
                  activeforeground="black",
                  command=lambda g=goal: self._open_edit(g)).pack(side="left")
        return card

    # ----- Actions -----
    def _open_add(self):
        color = next(self._color_cycle)
        _GoalDialog(self, self.app.model, color=color, on_save=self.refresh)

    def _open_edit(self, goal: dict):
        _GoalDialog(self, self.app.model, goal=goal, on_save=self.refresh)

    def _add_funds(self, goal: dict):
        _AddFundsDialog(
            self, goal,
            on_save=lambda amt: self._apply_funds(goal, amt),
        )

    def _apply_funds(self, goal: dict, amount: float):
        new_current = float(goal.get("current", 0)) + amount
        self.app.model.update_goal(goal["id"], current=new_current)
        self.refresh()

    def _delete(self, goal_id: int):
        if messagebox.askyesno("Confirm Delete", "Delete this goal?"):
            self.app.model.delete_goal(goal_id)
            self.refresh()

# ----- Goal dialog -----
class _GoalDialog(tk.Toplevel):
    def __init__(self, parent, model, goal=None, color=None, on_save=None):
        super().__init__(parent)
        self.model   = model
        self.goal    = goal
        self.color   = color or (goal["color"] if goal else COLORS["accent"])
        self.on_save = on_save

        self.title("Edit Goal" if goal else "New Goal")
        self.resizable(False, False)
        self.configure(bg=COLORS["card"])
        self.grab_set()
        self._center(400, 320)
        self._build()

    def _center(self, w, h):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        tk.Frame(self, bg=self.color, height=6).pack(fill="x")
        tk.Label(self, text="Edit Goal" if self.goal else "New Goal",
                 font=FONTS["subheading"], bg=COLORS["card"],
                 fg=COLORS["text"], pady=16).pack()
        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")

        form = tk.Frame(self, bg=COLORS["card"])
        form.pack(fill="both", expand=True, padx=30, pady=18)
        form.columnconfigure(0, weight=1)

        def field(lbl, key, row, default="0"):
            tk.Label(form, text=lbl, font=FONTS["body_bold"],
                     bg=COLORS["card"], fg=COLORS["text_muted"],
                     anchor="w").grid(row=row*2, column=0, sticky="w", pady=(8, 2))
            var = tk.StringVar(
                value=str(self.goal.get(key, default)) if self.goal else default)
            tk.Entry(form, textvariable=var, font=FONTS["body"], width=32,
                     relief="flat", bg=COLORS["bg"],
                     highlightthickness=1, highlightbackground=COLORS["border"],
                     highlightcolor=COLORS["primary"]).grid(
                         row=row*2+1, column=0, sticky="ew")
            return var

        self._name_var = field("Goal Name *", "name", 0, "")
        self._target_var = field("Target Amount ($) *", "target", 1, "")
        self._current_var = field("Current Saved ($)", "current", 2, "0")

        bf = tk.Frame(self, bg=COLORS["card"])
        bf.pack(fill="x", padx=30, pady=(0, 20))
        tk.Button(bf, text="Cancel", font=FONTS["button"],
                  bg=COLORS["border"], fg=COLORS["text"], relief="flat",
                  padx=18, pady=7, cursor="hand2",
                  command=self.destroy).pack(side="left")
        tk.Button(bf, text="Save Goal", font=FONTS["button"],
                  bg=COLORS["primary"], fg="black", relief="flat",
                  padx=18, pady=7, cursor="hand2",
                  activebackground=COLORS["primary_dark"], activeforeground="black",
                  command=self._save).pack(side="right")

    def _save(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showerror("Validation", "Goal name is required.", parent=self)
            return
        try:
            target  = float(self._target_var.get().replace(",", "").replace("$", ""))
            current = float(self._current_var.get().replace(",", "").replace("$", ""))
            if target <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation",
                                 "Please enter valid positive amounts.", parent=self)
            return

        if self.goal:
            self.model.update_goal(self.goal["id"],
                                   name=name, target=target, current=current)
        else:
            self.model.add_goal(name, target, current, self.color)

        if self.on_save:
            self.on_save()
        self.destroy()


# ----- Add Funds dialog -----

class _AddFundsDialog(tk.Toplevel):
    def __init__(self, parent, goal, on_save=None):
        super().__init__(parent)
        self.goal    = goal
        self.on_save = on_save

        self.title("Add Funds")
        self.resizable(False, False)
        self.configure(bg=COLORS["card"])
        self.grab_set()
        self._center(340, 210)
        self._build()

    def _center(self, w, h):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):
        color = self.goal.get("color", COLORS["accent"])
        tk.Frame(self, bg=color, height=6).pack(fill="x")
        tk.Label(self, text=f"Add Funds to '{self.goal['name']}'",
                 font=FONTS["subheading"], bg=COLORS["card"],
                 fg=COLORS["text"], pady=14, wraplength=300).pack()
        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")

        form = tk.Frame(self, bg=COLORS["card"])
        form.pack(fill="both", padx=28, pady=16)
        tk.Label(form, text="Amount to Add ($)", font=FONTS["body_bold"],
                 bg=COLORS["card"], fg=COLORS["text_muted"], anchor="w").pack(anchor="w")
        self._amt_var = tk.StringVar()
        tk.Entry(form, textvariable=self._amt_var, font=FONTS["body"], width=22,
                 relief="flat", bg=COLORS["bg"],
                 highlightthickness=1, highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["primary"]).pack(fill="x", pady=4, ipady=3)

        bf = tk.Frame(self, bg=COLORS["card"])
        bf.pack(fill="x", padx=28, pady=(0, 16))
        tk.Button(bf, text="Cancel", font=FONTS["button"],
                  bg=COLORS["border"], fg=COLORS["text"], relief="flat",
                  padx=14, pady=6, cursor="hand2",
                  command=self.destroy).pack(side="left")
        tk.Button(bf, text="Add Funds", font=FONTS["button"],
                  bg=COLORS["primary"], fg="black", relief="flat",
                  padx=14, pady=6, cursor="hand2",
                  activebackground=COLORS["primary_dark"], activeforeground="black",
                  command=self._save).pack(side="right")

    def _save(self):
        try:
            amt = float(self._amt_var.get().replace(",", "").replace("$", ""))
            if amt <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation",
                                 "Please enter a valid positive amount.", parent=self)
            return
        if self.on_save:
            self.on_save(amt)
        self.destroy()
