# 💰 Personal Budget Tracker

> **Your all-in-one desktop app for smart money management** — because adulting shouldn't be stressful!

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## ✨ Features

### 📊 **Dashboard** — Your Financial Overview at a Glance
- 🎯 Real-time statistics: monthly income, total expenses, and savings
- 📈 Interactive donut chart showing your savings allocation breakdown
- 📋 Recent expenses tracker (last 5 transactions)
- 💵 Savings breakdown table with category-wise allocation percentages

### 💳 **Expenses** — Track Every Dollar
- ➕ Add, edit, and delete expenses with ease
- 🏷️ Categorize expenses (Food, Transportation, Entertainment, Utilities, etc.)
- 🔍 Filter by category to find what you're looking for
- 📅 Date-stamped transactions with descriptions
- 💹 Category totals at a glance with quick-view pills

### 💵 **Savings** — Allocate Intelligently
- 🎨 Customizable savings allocation categories with color-coded swatches
- 🔄 Live preview of your savings pie chart as you adjust percentages
- ✅ Real-time validation (must sum to exactly 100%)
- 💰 Automatic dollar amount calculations per category
- 📊 Visual allocation breakdown

### 🎯 **Financial Goals** — Dream Big, Plan Smart
- 🏆 Create multiple financial goals with target amounts
- 📈 Progress bars showing how close you are to each goal
- ➕ Add funds to goals as you save
- 🎨 Auto-assigned color coding for visual organization
- ✏️ Edit goal details anytime
- 🗑️ Delete goals when complete or no longer relevant

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/PersonalBudgetTracker.git
   cd PersonalBudgetTracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

That's it! 🎉 The app window will open with a beautiful dashboard ready to go.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application logic |
| **Tkinter** | Modern, responsive desktop GUI |
| **Matplotlib** | Beautiful data visualization & charts |
| **JSON** | Persistent local data storage |

---

## 📁 Project Structure

```
PersonalBudgetTracker/
├── main.py                 # Application entry point
├── app.py                  # Root window & navigation
├── budget_data.json        # Local data persistence
├── requirements.txt        # Python dependencies
├── styles.py               # Design system (colors, fonts)
│
├── models/
│   ├── __init__.py
│   └── budget_model.py     # Data model & business logic
│
├── pages/
│   ├── __init__.py
│   ├── home_page.py        # Dashboard view
│   ├── expenses_page.py    # Expense management
│   ├── savings_page.py     # Savings allocation
│   └── goals_page.py       # Financial goals
│
└── utils/
    ├── __init__.py
    └── storage.py          # JSON data handling
```

---

## 💡 How It Works

### 🔄 Data Flow
1. **User Input** → Fills in expenses, sets income, updates savings allocation
2. **Data Processing** → `BudgetModel` validates and processes all changes
3. **Persistent Storage** → Changes auto-saved to `budget_data.json`
4. **UI Refresh** → Pages dynamically update to reflect latest data
5. **Visualizations** → Charts and stats render in real-time

### 🎨 Smart Features
- ✅ **Form Validation** — Prevents invalid monetary inputs
- 🔄 **Real-time Syncing** — All pages reflect updates instantly
- 📊 **Live Charts** — Donut charts redraw as you edit allocations
- 🎯 **Progress Tracking** — Goal completion visualized with progress bars
- 💾 **Auto-Save** — Your data persists when you close the app

---

## 📖 Usage Guide

### Setting Up Your Budget

1. **Enter Monthly Income** 💸
   - On the Dashboard, set your monthly income in the top-right field
   - Click "Set" to confirm

2. **Add Your Expenses** 📝
   - Navigate to **Expenses** tab
   - Click "+ Add Expense"
   - Fill in date, description, category, and amount
   - Categorize intelligently (Food, Transportation, etc.)

3. **Allocate Your Savings** 🏦
   - Go to **Savings Allocation** tab
   - Create categories (e.g., Emergency Fund, Vacation, Down Payment)
   - Adjust percentages so they sum to exactly 100%
   - Watch the live preview chart update in real-time
   - Click "💾 Save Allocations" when happy

4. **Set Financial Goals** 🎯
   - Visit **Goals** tab
   - Click "+ New Goal"
   - Enter goal name, target amount, and current saved amount
   - Click "➕ Add Funds" as you progress toward each goal
   - Celebrate when you hit 100%! 🎉

---

## 🎯 For Recruiters & Developers

### What This Project Demonstrates

✅ **Clean Architecture**
- Separation of concerns (models, views, utilities)
- Modular, reusable components
- Clear naming conventions

✅ **User Experience Focus**
- Intuitive navigation with a responsive sidebar
- Consistent design language throughout
- Real-time validation and helpful error messages
- Beautiful, accessible color scheme

✅ **Software Engineering Best Practices**
- Data persistence with JSON
- Form validation and error handling
- Event-driven architecture with callbacks
- DRY principle (Don't Repeat Yourself)

✅ **Problem-Solving Skills**
- Manages complex state across multiple views
- Handles datetime parsing and formatting
- Implements live chart updates with Matplotlib
- Optimizes layout with smart geometry management

---

## 🚀 Future Enhancements

- 📱 Mobile app version (React Native)
- 📊 Advanced analytics & spending reports
- 🔐 User authentication & cloud sync
- 📧 Budget alerts & notifications
- 📥 CSV import/export for expenses
- 🌙 Dark mode theme
- 💬 Budget recommendations based on spending patterns

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute!

---

## 👋 Contributing

Have ideas or found a bug? Contributions are welcome!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

⭐ **Star this repo if you found it helpful!**

</div>
