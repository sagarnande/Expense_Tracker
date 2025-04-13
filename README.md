# Expense Tracker (Streamlit + SQLite)

This is a simple and user-friendly **Expense Tracker Web App** built using **Python**, **Streamlit**, and **SQLite**. It allows users to register, log in, add daily expenses, and visualize their spending patterns through daily, weekly, and monthly reports with pie charts.

---

##  Features

- ✅ User Registration & Login
- ✍️ Add and View Daily Expenses
- 📅 Filter Expenses by Date and Category
- 🗑️ Delete Specific Expense Entries
- 📊 Visual Reports:
  - Daily, Weekly, and Monthly Total Charts
  - Category-wise Pie Charts for Daily, Weekly, and Monthly Spending
- 📦 Lightweight SQLite backend for storing data

---

##  Technologies Used

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/index.html)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

---

##  Installation & Run

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
2. Create Virtual Environment (optional but recommended)
bash
Copy
Edit
python -m venv .venv
.\.venv\Scripts\activate  # For Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If you don’t have a requirements.txt, you can install manually:

bash
Copy
Edit
pip install streamlit pandas matplotlib
4. Run the App
bash
Copy
Edit
streamlit run Expense.py
Or (if streamlit command not recognized):

bash
Copy
Edit
python -m streamlit run Expense.py
```
##📁 Project Structure
bash
Copy
Edit
├── Expense.py             # Main Streamlit App
├── expenses.db            # SQLite Database (auto-created)
├── .venv/                 # Virtual Environment (optional)
└── README.md              # Project Documentation
└── requirements.txt       # Requirements files
🙌 Author
Developed by Nande Sagar — a passionate developer building practical apps with Python and Streamlit.

📃 License
This project is open-source and available under the MIT License.
