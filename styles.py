# styles.py
# Centralized color palette, typography, and constants.

COLORS = {
    # Brand greens
    "primary":       "#2d6a4f",
    "primary_dark":  "#1b4332",
    "primary_light": "#52b788",
    # Accent
    "accent":        "#4895ef",
    "accent_dark":   "#2d6bbf",
    # Semantic
    "success":       "#40916c",
    "danger":        "#e63946",
    "warning":       "#f4a261",
    # Surfaces
    "bg":            "#f0f4f8",
    "card":          "#ffffff",
    "sidebar":       "#1b4332",
    "sidebar_hover": "#2d6a4f",
    "row_alt":       "#f7faf8",
    "border":        "#e2e8f0",
    # Text
    "text":          "#1a1a2e",
    "text_muted":    "#6c757d",
    "text_light":    "#adb5bd",
    # Table
    "th_bg":         "#2d6a4f",
    "th_fg":         "#ffffff",
}

FONTS = {
    "app_title":    ("Helvetica", 15, "bold"),
    "heading":      ("Helvetica", 20, "bold"),
    "subheading":   ("Helvetica", 13, "bold"),
    "card_title":   ("Helvetica", 10),
    "card_value":   ("Helvetica", 23, "bold"),
    "body":         ("Helvetica", 11),
    "body_bold":    ("Helvetica", 11, "bold"),
    "small":        ("Helvetica", 9),
    "small_bold":   ("Helvetica", 9, "bold"),
    "button":       ("Helvetica", 10, "bold"),
    "table_header": ("Helvetica", 10, "bold"),
    "table_body":   ("Helvetica", 10),
    "sidebar_item": ("Helvetica", 11),
    "nav_active":   ("Helvetica", 11, "bold"),
}

EXPENSE_CATEGORIES = [
    "Housing",
    "Transportation",
    "Food & Groceries",
    "Utilities",
    "Healthcare",
    "Entertainment",
    "Education",
    "Debt Payments",
    "Insurance",
    "Shopping",
    "Subscriptions",
    "Other",
]

# Cycling colors assigned to new goals
GOAL_COLORS = [
    "#4895ef",
    "#52b788",
    "#f4a261",
    "#e63946",
    "#9b59b6",
    "#1abc9c",
    "#e67e22",
    "#16a085",
]

# Default savings allocation splits
DEFAULT_ALLOCATIONS = [
    {"name": "Savings",    "percent": 40, "color": "#52b788"},
    {"name": "Emergency",  "percent": 25, "color": "#4895ef"},
    {"name": "Debt Payoff","percent": 20, "color": "#f4a261"},
    {"name": "Other Goals","percent": 15, "color": "#e63946"},
]
