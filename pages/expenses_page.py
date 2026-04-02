# pages/expenses_page.py
# Full expense management: add, edit, delete, filter, totals.

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date as dt_date
from styles import COLORS, FONTS, EXPENSE_CATEGORIES

class ExpensesPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._build()

    # ----- Build -----
    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=32, pady=(24, 14))
        tk.Label(hdr, text="Expenses", font=FONTS["heading"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(side="left")
        _PrimaryBtn(hdr, "+ Add Expense", self._add).pack(side="right")

        # Filter bar
        fbar = tk.Frame(self, bg=COLORS["bg"])
        fbar.pack(fill="x", padx=32, pady=(0, 12))

        tk.Label(fbar, text="Filter by category:", font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["text_muted"]).pack(side="left")

        self._filter_var = tk.StringVar(value="All")
        cats = ["All"] + EXPENSE_CATEGORIES
        cb = ttk.Combobox(fbar, textvariable=self._filter_var,
                          values=cats, state="readonly", width=20,
                          font=FONTS["body"])
        cb.pack(side="left", padx=8)
        cb.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        # Category totals (small pill strip)
        self._pill_frame = tk.Frame(fbar, bg=COLORS["bg"])
        self._pill_frame.pack(side="right")

        # Main card
        card = tk.Frame(self, bg=COLORS["card"],
                        highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=32, pady=(0, 16))

        # Table column headers
        col_names = ["Date", "Description", "Category", "Amount", "Actions"]
        hdr_row = tk.Frame(card, bg=COLORS["th_bg"])
        hdr_row.pack(fill="x")
        weights = [1, 3, 2, 1, 2]
        for name, w in zip(col_names, weights):
            tk.Label(hdr_row, text=name, font=FONTS["table_header"],
                     bg=COLORS["th_bg"], fg=COLORS["th_fg"],
                     pady=10, padx=10, anchor="w").pack(
                         side="left", expand=True, fill="both")

        # Scrollable body
        body_wrap = tk.Frame(card, bg=COLORS["card"])
        body_wrap.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(body_wrap, bg=COLORS["card"], highlightthickness=0)
        vsb = ttk.Scrollbar(body_wrap, orient="vertical", command=self._canvas.yview)
        self._rows_frame = tk.Frame(self._canvas, bg=COLORS["card"])
        self._rows_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.create_window((0, 0), window=self._rows_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)
        self._canvas.bind("<Enter>",
            lambda _: self._canvas.bind_all("<MouseWheel>", self._scroll))
        self._canvas.bind("<Leave>",
            lambda _: self._canvas.unbind_all("<MouseWheel>"))

        # Footer totals bar
        self._footer = tk.Frame(card, bg=COLORS["primary_dark"])
        self._footer.pack(fill="x", side="bottom")
        self._total_lbl = tk.Label(
            self._footer,
            text="Total Expenses:   $0.00",
            font=FONTS["body_bold"],
            bg=COLORS["primary_dark"], fg="white",
            pady=9, padx=20, anchor="e",
        )
        self._total_lbl.pack(fill="x")

    def _scroll(self, event):
        self._canvas.yview_scroll(-1 * (event.delta // 120), "units")

    # ----- Refresh -----
    def refresh(self):
        for w in self._rows_frame.winfo_children():
            w.destroy()

        expenses = self.app.model.expenses
        filt = self._filter_var.get()
        if filt != "All":
            expenses = [e for e in expenses if e.get("category") == filt]

        expenses_sorted = sorted(expenses,
                                 key=lambda x: x.get("date", ""), reverse=True)

        if not expenses_sorted:
            tk.Label(self._rows_frame,
                     text="No expenses found. Click '+ Add Expense' to get started.",
                     font=FONTS["body"], bg=COLORS["card"],
                     fg=COLORS["text_muted"], pady=32).pack()
        else:
            for i, exp in enumerate(expenses_sorted):
                self._build_row(i, exp)

        total = sum(e["amount"] for e in expenses)
        self._total_lbl.config(text=f"Total Expenses:   ${total:,.2f}")

        # Update category pills
        self._rebuild_pills()

    def _rebuild_pills(self):
        for w in self._pill_frame.winfo_children():
            w.destroy()

        by_cat = self.app.model.expenses_by_category()
        for cat, total in sorted(by_cat.items(), key=lambda x: -x[1])[:4]:
            pill = tk.Frame(self._pill_frame, bg=COLORS["primary_light"],
                            highlightthickness=0)
            pill.pack(side="left", padx=3)
            tk.Label(pill, text=f"{cat}  ${total:,.0f}",
                     font=FONTS["small"], bg=COLORS["primary_light"],
                     fg="white", padx=8, pady=3).pack()

    # ----- Row -----

    def _build_row(self, idx, exp):
        bg = COLORS["row_alt"] if idx % 2 else COLORS["card"]
        row = tk.Frame(self._rows_frame, bg=bg)
        row.pack(fill="x", padx=2, pady=1)

        values = [exp.get("date", "—"), exp.get("description", ""),
                  exp.get("category", ""), f"${exp['amount']:,.2f}"]
        fgs = [COLORS["text"], COLORS["text"], COLORS["text_muted"], COLORS["danger"]]
        weights = [1, 3, 2, 1]

        for val, fg, w in zip(values, fgs, weights):
            tk.Label(row, text=val, font=FONTS["table_body"],
                     bg=bg, fg=fg, pady=9, padx=10, anchor="w").pack(
                         side="left", expand=True, fill="both")

        # Action buttons
        act = tk.Frame(row, bg=bg)
        act.pack(side="left", expand=True, fill="both", padx=6)

        tk.Button(act, text="✎  Edit", font=FONTS["small_bold"],
                  bg=COLORS["accent"], fg="black", relief="flat",
                  padx=9, pady=4, cursor="hand2",
                  activebackground=COLORS["accent_dark"], activeforeground="black",
                  command=lambda e=exp: self._edit(e)).pack(side="left", padx=(0, 5), pady=7)

        tk.Button(act, text="✕  Delete", font=FONTS["small_bold"],
                  bg=COLORS["danger"], fg="black", relief="flat",
                  padx=9, pady=4, cursor="hand2",
                  activebackground="#c0392b", activeforeground="black",
                  command=lambda eid=exp["id"]: self._delete(eid)).pack(side="left", pady=7)

    # ----- Actions -----
    def _add(self):
        _ExpenseDialog(self, self.app.model, on_save=self.refresh)

    def _edit(self, expense):
        _ExpenseDialog(self, self.app.model, expense=expense, on_save=self.refresh)

    def _delete(self, expense_id):
        if messagebox.askyesno("Confirm Delete",
                                "Are you sure you want to delete this expense?"):
            self.app.model.delete_expense(expense_id)
            self.refresh()


# ----- Add / Edit dialog -----
class _ExpenseDialog(tk.Toplevel):
    def __init__(self, parent, model, expense=None, on_save=None):
        super().__init__(parent)
        self.model   = model
        self.expense = expense
        self.on_save = on_save

        self.title("Edit Expense" if expense else "Add Expense")
        self.resizable(False, False)
        self.configure(bg=COLORS["card"])
        self.grab_set()
        self._center(440, 400)
        self._build()

    def _center(self, w, h):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw - w)//2}+{(sh - h)//2}")

    def _build(self):
        # Title bar
        tk.Frame(self, bg=COLORS["primary"], height=6).pack(fill="x")
        tk.Label(self,
                 text="✎  Edit Expense" if self.expense else "➕  Add Expense",
                 font=FONTS["subheading"], bg=COLORS["card"],
                 fg=COLORS["text"], pady=16).pack()
        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x")

        form = tk.Frame(self, bg=COLORS["card"])
        form.pack(fill="both", expand=True, padx=30, pady=20)
        form.columnconfigure(0, weight=1)

        def entry_field(lbl, key, row, default=""):
            tk.Label(form, text=lbl, font=FONTS["body_bold"],
                     bg=COLORS["card"], fg=COLORS["text_muted"],
                     anchor="w").grid(row=row*2, column=0, sticky="w", pady=(8, 2))
            var = tk.StringVar(value=str(self.expense.get(key, default))
                               if self.expense else default)
            e = tk.Entry(form, textvariable=var, font=FONTS["body"], width=34,
                         relief="flat", bg=COLORS["bg"],
                         highlightthickness=1,
                         highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["primary"])
            e.grid(row=row*2+1, column=0, sticky="ew")
            return var

        def combo_field(lbl, key, row):
            tk.Label(form, text=lbl, font=FONTS["body_bold"],
                     bg=COLORS["card"], fg=COLORS["text_muted"],
                     anchor="w").grid(row=row*2, column=0, sticky="w", pady=(8, 2))
            var = tk.StringVar(value=self.expense.get(key, "") if self.expense else "")
            cb = ttk.Combobox(form, textvariable=var,
                              values=EXPENSE_CATEGORIES, state="readonly",
                              font=FONTS["body"], width=33)
            cb.grid(row=row*2+1, column=0, sticky="ew")
            return var

        self._desc_var = entry_field("Description *", "description", 0)
        self._cat_var = combo_field("Category *", "category", 1)
        self._amt_var = entry_field("Amount ($) *", "amount", 2,
                                     default=str(self.expense.get("amount", ""))
                                     if self.expense else "")
        self._date_var = entry_field("Date (YYYY-MM-DD)", "date", 3,
                                     default=dt_date.today().strftime("%Y-%m-%d"))

        # Buttons
        bf = tk.Frame(self, bg=COLORS["card"])
        bf.pack(fill="x", padx=30, pady=(0, 22))
        tk.Button(bf, text="Cancel", font=FONTS["button"], bg=COLORS["border"],
                  fg=COLORS["text"], relief="flat", padx=18, pady=8, cursor="hand2",
                  command=self.destroy).pack(side="left")
        tk.Button(bf, text="Save Expense", font=FONTS["button"], bg=COLORS["primary"],
                  fg="black", relief="flat", padx=18, pady=8, cursor="hand2",
                  activebackground=COLORS["primary_dark"], activeforeground="black",
                  command=self._save).pack(side="right")

    def _save(self):
        desc = self._desc_var.get().strip()
        cat  = self._cat_var.get().strip()
        raw  = self._amt_var.get().strip().replace(",", "").replace("$", "")
        date = self._date_var.get().strip()

        if not desc:
            messagebox.showerror("Validation", "Description is required.", parent=self)
            return
        if not cat:
            messagebox.showerror("Validation", "Please select a category.", parent=self)
            return
        try:
            amount = float(raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation", "Amount must be a positive number.", parent=self)
            return

        if self.expense:
            self.model.update_expense(self.expense["id"],
                                      description=desc, category=cat,
                                      amount=amount, date=date)
        else:
            self.model.add_expense(desc, cat, amount, date)

        if self.on_save:
            self.on_save()
        self.destroy()


# ----- Shared helper -----

class _PrimaryBtn(tk.Button):
    def __init__(self, parent, text, cmd):
        super().__init__(parent, text=text, command=cmd, cursor="hand2",
            font=FONTS["button"], bg=COLORS["primary"], fg="black", relief="flat",
            padx=16, pady=8, activebackground=COLORS["primary_dark"], activeforeground="black")
