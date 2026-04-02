# pages/home_page.py
# Dashboard: stat cards, savings breakdown, donut chart, recent expenses.

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from styles import COLORS, FONTS

class HomePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._chart_fig    = None
        self._chart_canvas = None
        self._build()

    def _build(self):
        # ----- Page header -----
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=32, pady=(24, 12))

        tk.Label(hdr, text="Dashboard", font=FONTS["heading"], bg=COLORS["bg"],
                 fg=COLORS["text"]).pack(side="left")

        # Inline income setter
        setter = tk.Frame(hdr, bg=COLORS["bg"])
        setter.pack(side="right")
        tk.Label(setter, text="Monthly Income  $", font=FONTS["body"], bg=COLORS["bg"],
                 fg=COLORS["text_muted"]).pack(side="left")
        self._income_var = tk.StringVar()
        tk.Entry(setter, textvariable=self._income_var, width=11, font=FONTS["body_bold"],
                 relief="flat", bg="white", highlightthickness=1, highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["primary"],).pack(side="left", padx=5)
        _btn(setter, "Set", self._set_income, small=True).pack(side="left")

        # ----- Stat cards -----
        cards = tk.Frame(self, bg=COLORS["bg"])
        cards.pack(fill="x", padx=32, pady=(0, 16))
        self._c_income  = _StatCard(cards, "Monthly Income",  COLORS["primary"])
        self._c_expense = _StatCard(cards, "Total Expenses",  COLORS["danger"])
        self._c_savings = _StatCard(cards, "Total Savings",   COLORS["accent"])
        for c in (self._c_income, self._c_expense, self._c_savings):
            c.pack(side="left", expand=True, fill="both", padx=7)

        # ----- Middle row -----
        mid = tk.Frame(self, bg=COLORS["bg"])
        mid.pack(fill="both", expand=True, padx=32, pady=(0, 16))

        # Breakdown card
        bk = _Card(mid, "💵  Savings Breakdown")
        bk.pack(side="left", fill="both", expand=True, padx=(0, 9))
        self._bk_body = tk.Frame(bk.body, bg=COLORS["card"])
        self._bk_body.pack(fill="both", expand=True, padx=12, pady=10)

        # Chart card
        ch = _Card(mid, "📊  Savings Allocation Chart")
        ch.pack(side="left", fill="both", expand=True, padx=(9, 0))
        self._ch_body = ch.body

        # ----- Recent expenses -----
        rc = _Card(self, "🕒  Recent Expenses (last 5)")
        rc.pack(fill="x", padx=32, pady=(0, 22))
        self._rc_body = rc.body

    # ----- Actions -----
    def _set_income(self):
        try:
            val = float(self._income_var.get().replace(",", "").replace("$", ""))
            if val < 0:
                raise ValueError
            self.app.model.income = val
            self.refresh()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for income.")

    # ----- Refresh -----
    def refresh(self):
        m   = self.app.model
        inc = m.income
        exp = m.total_expenses
        sav = m.total_savings
        alloc = m.savings_allocations

        self._income_var.set(f"{inc:,.2f}")
        self._c_income.set(f"${inc:,.2f}")
        self._c_expense.set(f"${exp:,.2f}")
        self._c_savings.set(f"${sav:,.2f}")
        self._refresh_breakdown(alloc, sav)
        self._refresh_chart(alloc, sav)
        self._refresh_recent(m.expenses)

    # ----- Breakdown table -----

    def _refresh_breakdown(self, allocations, savings):
        for w in self._bk_body.winfo_children():
            w.destroy()

        _ThRow(self._bk_body, ["Category", "%", "Amount"]).pack(fill="x", pady=(0, 2))

        for i, a in enumerate(allocations):
            dollar = savings * a["percent"] / 100
            _TdRow(
                self._bk_body,
                [f"  ● {a['name']}", f"{a['percent']}%", f"${dollar:,.2f}"],
                alt=(i % 2 == 1),
                fg0=a["color"],
            ).pack(fill="x", pady=1)

        # Totals row
        _ThRow(
            self._bk_body,
            ["  Total", "100%", f"${savings:,.2f}"],
            bg=COLORS["primary_dark"],
        ).pack(fill="x", pady=(2, 0))

    # ----- Donut chart -----
    def _refresh_chart(self, allocations, savings):
        # Tear down previous chart
        for w in self._ch_body.winfo_children():
            w.destroy()
        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
            self._chart_canvas = None
        if self._chart_fig:
            plt.close(self._chart_fig)
            self._chart_fig = None

        if savings <= 0 or not allocations:
            tk.Label(
                self._ch_body,
                text="Set your income and\nrecord expenses to see\nyour savings chart.",
                font=FONTS["body"], bg=COLORS["card"],
                fg=COLORS["text_muted"], justify="center",
            ).pack(expand=True)
            return

        fig, ax = plt.subplots(figsize=(3.4, 2.8), facecolor=COLORS["card"])
        ax.set_facecolor(COLORS["card"])

        sizes  = [a["percent"] for a in allocations]
        colors = [a["color"]   for a in allocations]
        labels = [a["name"]    for a in allocations]

        wedges, _, auto = ax.pie(
            sizes, labels=None, colors=colors,
            autopct="%1.0f%%", startangle=90,
            pctdistance=0.74,
            wedgeprops=dict(width=0.46, edgecolor="white", linewidth=2),
        )
        for at in auto:
            at.set_fontsize(8)
            at.set_color("white")
            at.set_fontweight("bold")

        ax.legend(wedges, labels, loc="lower center",
                  bbox_to_anchor=(0.5, -0.18),
                  ncol=2, fontsize=7, frameon=False)
        fig.tight_layout(pad=0.6)

        canvas = FigureCanvasTkAgg(fig, master=self._ch_body)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        self._chart_fig    = fig
        self._chart_canvas = canvas

    # ----- Recent expenses table -----
    def _refresh_recent(self, expenses):
        for w in self._rc_body.winfo_children():
            w.destroy()

        wrap = tk.Frame(self._rc_body, bg=COLORS["card"])
        wrap.pack(fill="x", padx=12, pady=10)

        _ThRow(wrap, ["Date", "Description", "Category", "Amount"],
               weights=[1, 3, 2, 1]).pack(fill="x", pady=(0, 2))
        recent = sorted(expenses, key=lambda x: x.get("date", ""), reverse=True)[:5]

        if not recent:
            tk.Label(wrap, text="No expenses recorded yet. Go to Expenses to add some!",
                     font=FONTS["body"], bg=COLORS["card"], fg=COLORS["text_muted"], pady=18).pack()
            return

        for i, e in enumerate(recent):
            _TdRow(
                wrap,
                [e.get("date", "—"), e.get("description", ""),
                 e.get("category", ""), f"${e['amount']:,.2f}"],
                alt=(i % 2 == 1),
                weights=[1, 3, 2, 1],
                fg3=COLORS["danger"],
            ).pack(fill="x", pady=1)
        tk.Frame(wrap, bg=COLORS["card"], height=6).pack()


# ----- Shared sub-widgets -----
def _btn(parent, text, cmd, small=False):
    return tk.Button(
        parent, text=text, command=cmd, cursor="hand2",
        font=FONTS["small_bold"] if small else FONTS["button"],
        bg=COLORS["primary"], fg="black", relief="flat",
        padx=10, pady=6 if small else 7,
        activebackground=COLORS["primary_dark"],
        activeforeground="black",
    )


class _StatCard(tk.Frame):
    def __init__(self, parent, title, color):
        super().__init__(parent, bg=COLORS["card"],
                         highlightbackground=COLORS["border"], highlightthickness=1)
        tk.Frame(self, bg=color, height=5).pack(fill="x")
        tk.Label(self, text=title, font=FONTS["card_title"],
                 bg=COLORS["card"], fg=COLORS["text_muted"]).pack(pady=(13, 4))
        self._val = tk.Label(self, text="$0.00", font=FONTS["card_value"],
                              bg=COLORS["card"], fg=color)
        self._val.pack(pady=(0, 14))

    def set(self, text: str):
        self._val.config(text=text)


class _Card(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, bg=COLORS["card"],
                         highlightbackground=COLORS["border"], highlightthickness=1)
        tk.Label(self, text=title, font=FONTS["subheading"],
                 bg=COLORS["card"], fg=COLORS["text"],
                 padx=16, pady=11, anchor="w").pack(fill="x")
        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")
        self.body = tk.Frame(self, bg=COLORS["card"])
        self.body.pack(fill="both", expand=True)


class _ThRow(tk.Frame):
    """Table header row."""
    def __init__(self, parent, labels, bg=None, weights=None):
        _bg = bg or COLORS["th_bg"]
        super().__init__(parent, bg=_bg)
        weights = weights or [1] * len(labels)
        for i, (lbl, w) in enumerate(zip(labels, weights)):
            anchor = "w" if i == 0 else "e"
            tk.Label(self, text=lbl, font=FONTS["table_header"],
                     bg=_bg, fg=COLORS["th_fg"],
                     pady=8, padx=10, anchor=anchor).pack(
                         side="left", expand=True, fill="both")


class _TdRow(tk.Frame):
    """Table data row with optional column-specific fg colours."""
    def __init__(self, parent, values, alt=False, weights=None,
                 fg0=None, fg3=None):
        bg = COLORS["row_alt"] if alt else COLORS["card"]
        super().__init__(parent, bg=bg)
        weights = weights or [1] * len(values)
        for i, (val, w) in enumerate(zip(values, weights)):
            fg = COLORS["text"]
            if i == 0 and fg0:
                fg = fg0
            elif i == 3 and fg3:
                fg = fg3
            anchor = "w" if i == 0 else "e"
            tk.Label(self, text=val, font=FONTS["table_body"],
                     bg=bg, fg=fg, pady=8, padx=10, anchor=anchor).pack(
                         side="left", expand=True, fill="both")