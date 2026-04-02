# pages/savings_page.py
# Edit savings allocation percentages with a live updating donut chart.

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from styles import COLORS, FONTS

class SavingsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._rows: list = []
        self._chart_fig = None
        self._chart_canvas = None
        self._build()

    # ----- Build -----
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=32, pady=(24, 14))
        tk.Label(hdr, text="Savings Allocation", font=FONTS["heading"], bg=COLORS["bg"],
                 fg=COLORS["text"]).pack(side="left")
        tk.Button(hdr, text="💾  Save Allocations", font=FONTS["button"],
                  bg=COLORS["primary"], fg="black", relief="flat",
                  padx=16, pady=8, cursor="hand2", activebackground=COLORS["primary_dark"],
                  activeforeground="black", command=self._save_alloc).pack(side="right")

        # Summary strip
        strip = tk.Frame(self, bg=COLORS["primary"])
        strip.pack(fill="x", padx=32, pady=(0, 16))
        self._sum_labels: dict = {}
        for key, label in [("income", "Monthly Income"), ("expenses", "Total Expenses"),
                           ("savings", "Available to Allocate")]:
            col = tk.Frame(strip, bg=COLORS["primary"])
            col.pack(side="left", expand=True, pady=12)
            tk.Label(col, text=label, font=FONTS["small"], bg=COLORS["primary"], fg="#a8d8c0").pack()
            lbl = tk.Label(col, text="$0.00", font=FONTS["body_bold"], bg=COLORS["primary"], fg="white")
            lbl.pack()
            self._sum_labels[key] = lbl

        # Content row
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(fill="both", expand=True, padx=32, pady=(0, 16))

        # Left: allocation table
        tbl_card = tk.Frame(content, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1)
        tbl_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(tbl_card, text="Allocation Settings", font=FONTS["subheading"],
                 bg=COLORS["card"], fg=COLORS["text"], padx=16, pady=12, anchor="w").pack(fill="x")
        tk.Frame(tbl_card, bg=COLORS["border"], height=1).pack(fill="x")
        self._tbl_body = tk.Frame(tbl_card, bg=COLORS["card"])
        self._tbl_body.pack(fill="both", expand=True, padx=14, pady=12)

        # Right: chart
        ch_card = tk.Frame(content, bg=COLORS["card"],
                           highlightbackground=COLORS["border"], highlightthickness=1)
        ch_card.pack(side="left", fill="both", expand=True, padx=(10, 0))
        tk.Label(ch_card, text="Live Preview", font=FONTS["subheading"], bg=COLORS["card"],
                 fg=COLORS["text"], padx=16, pady=12, anchor="w").pack(fill="x")
        tk.Frame(ch_card, bg=COLORS["border"], height=1).pack(fill="x")
        self._ch_body = tk.Frame(ch_card, bg=COLORS["card"])
        self._ch_body.pack(fill="both", expand=True)

        # Percentage validation label
        foot = tk.Frame(self, bg=COLORS["bg"])
        foot.pack(fill="x", padx=32, pady=(0, 8))
        self._pct_lbl = tk.Label(foot, text="", font=FONTS["small"], bg=COLORS["bg"], fg=COLORS["text_muted"])
        self._pct_lbl.pack(side="right")

    # ----- Refresh -----
    def refresh(self):
        m = self.app.model
        self._sum_labels["income"].config(text=f"${m.income:,.2f}")
        self._sum_labels["expenses"].config(text=f"${m.total_expenses:,.2f}")
        self._sum_labels["savings"].config(text=f"${m.total_savings:,.2f}")

        # Rebuild rows
        for w in self._tbl_body.winfo_children():
            w.destroy()
        self._rows = []

        # Column header
        hdr = tk.Frame(self._tbl_body, bg=COLORS["th_bg"])
        hdr.pack(fill="x", pady=(0, 6))
        for col, w in [("Category Name", 18), ("Swatch", 6), ("%", 7), ("Amount", 13)]:
            tk.Label(hdr, text=col, font=FONTS["table_header"], bg=COLORS["th_bg"],
                     fg=COLORS["th_fg"], width=w, pady=8).pack(side="left", expand=True, fill="both")

        for a in m.savings_allocations:
            self._add_alloc_row(a)
        self._update_chart()

    # ----- Row -----
    def _add_alloc_row(self, alloc: dict):
        row = tk.Frame(self._tbl_body, bg=COLORS["card"])
        row.pack(fill="x", pady=4)

        name_var = tk.StringVar(value=alloc["name"])
        pct_var  = tk.StringVar(value=str(alloc["percent"]))
        color    = alloc["color"]

        # Name entry
        tk.Entry(row, textvariable=name_var, font=FONTS["body"], width=16, relief="flat",
                 bg=COLORS["bg"], highlightthickness=1, highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["primary"]).pack(side="left", padx=4, ipady=4)

        # Color swatch
        tk.Label(row, bg=color, width=5, highlightthickness=1, 
                 highlightbackground=COLORS["border"]).pack(side="left", padx=4, ipady=14)

        # Percent entry
        tk.Entry(row, textvariable=pct_var, font=FONTS["body_bold"], width=6, justify="center",
                 relief="flat", bg=COLORS["bg"], highlightthickness=1, highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["primary"]).pack(side="left", padx=4, ipady=4)
        tk.Label(row, text="%", font=FONTS["body"], bg=COLORS["card"], fg=COLORS["text_muted"]).pack(side="left")

        # Auto dollar label
        dollar_lbl = tk.Label(row, text="$0.00", font=FONTS["body"], bg=COLORS["card"],
                              fg=COLORS["primary_dark"], width=12, anchor="e", padx=10)
        dollar_lbl.pack(side="left", padx=6)

        # Trigger live chart refresh on every keystroke
        pct_var.trace_add("write", lambda *_: self._update_chart())
        self._rows.append({"name_var": name_var, "pct_var": pct_var, "color": color, "dollar_lbl": dollar_lbl})

    # ----- Live chart update -----
    def _update_chart(self):
        savings   = self.app.model.total_savings
        total_pct = 0.0
        all_valid = True

        for row in self._rows:
            try:
                pct = float(row["pct_var"].get())
                if pct < 0:
                    raise ValueError
                total_pct += pct
                row["dollar_lbl"].config(
                    text=f"${savings * pct / 100:,.2f}", fg=COLORS["primary_dark"])
            except ValueError:
                row["dollar_lbl"].config(text="—", fg=COLORS["danger"])
                all_valid = False

        # Percentage status label
        if not all_valid:
            self._pct_lbl.config(text="⚠  Invalid value entered", fg=COLORS["danger"])
        elif abs(total_pct - 100) > 0.01:
            self._pct_lbl.config(
                text=f"⚠  Currently {total_pct:.1f}%  — must equal 100%",
                fg=COLORS["danger"])
        else:
            self._pct_lbl.config(text="✓  Percentages sum to 100%",
                                  fg=COLORS["success"])

        # Rebuild chart
        for w in self._ch_body.winfo_children():
            w.destroy()
        if self._chart_canvas:
            self._chart_canvas.get_tk_widget().destroy()
            self._chart_canvas = None
        if self._chart_fig:
            plt.close(self._chart_fig)
            self._chart_fig = None

        try:
            sizes  = [float(r["pct_var"].get()) for r in self._rows]
            colors = [r["color"] for r in self._rows]
            labels = [r["name_var"].get() for r in self._rows]
        except ValueError:
            return

        if not sizes or any(s <= 0 for s in sizes):
            return

        fig, ax = plt.subplots(figsize=(3.6, 3.0), facecolor=COLORS["card"])
        ax.set_facecolor(COLORS["card"])
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
                  bbox_to_anchor=(0.5, -0.20), ncol=2, fontsize=7, frameon=False)
        fig.tight_layout(pad=0.6)

        canvas = FigureCanvasTkAgg(fig, master=self._ch_body)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        self._chart_fig    = fig
        self._chart_canvas = canvas

    # ----- Save -----
    def _save_alloc(self):
        rows, total = [], 0.0
        for row in self._rows:
            try:
                pct = float(row["pct_var"].get())
                if pct < 0:
                    raise ValueError
                total += pct
            except ValueError:
                messagebox.showerror("Validation", "All percentages must be valid positive numbers.")
                return
            rows.append({
                "name":    row["name_var"].get().strip() or "Unnamed",
                "percent": pct,
                "color":   row["color"],
            })

        if abs(total - 100) > 0.01:
            messagebox.showerror("Validation",
                f"Percentages must sum to exactly 100%.\nCurrent total: {total:.1f}%",)
            return

        self.app.model.update_savings_allocations(rows)
        messagebox.showinfo("Saved", "✓  Savings allocations saved successfully!")
