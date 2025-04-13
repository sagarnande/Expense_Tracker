import sqlite3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Create a database connection function
def get_db_conn():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

# Create tables if they do not exist
def create_tables():
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        description TEXT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id))
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Login a user
def login_user(username, password):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Add a new expense
def add_expense(date, category, amount, description, user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount, description, user_id) VALUES(?, ?, ?, ?, ?)",
                   (date, category, amount, description, user_id))
    conn.commit()
    conn.close()

# Get all expenses for a user
def get_expenses(user_id):
    conn = get_db_conn()  # This should return a valid SQLite connection
    df = pd.read_sql_query("SELECT * FROM expenses WHERE user_id=?", conn, params=(user_id,))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Get daily total expenses for a user
def get_daily_total(user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT date, SUM(amount) AS total FROM expenses WHERE user_id=? GROUP BY date", conn, params=(user_id,))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Get expenses by category for a user
def get_expenses_by_category(category, user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT * FROM expenses WHERE category=? AND user_id=?", conn, params=(category, user_id))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Get expenses by date for a user
def get_expense_by_date(date, user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT * FROM expenses WHERE date=? AND user_id=?", conn, params=(date, user_id))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Get monthly total expenses for a user
def get_monthly_total(user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total FROM expenses WHERE user_id=? GROUP BY month", conn, params=(user_id,))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Get weekly total expenses for a user
def get_weekly_total(user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT strftime('%Y-%U', date) AS week, SUM(amount) AS total FROM expenses WHERE user_id=? GROUP BY week", conn, params=(user_id,))
    conn.close()
    df.index = range(1, len(df) + 1)
    return df

# Delete an expense
def delete_expense(expense_id, user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (expense_id, user_id))
    conn.commit()
    conn.close()

# Generate an expense report for a user
def generate_report(user_id):
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT category, SUM(amount) AS total FROM expenses WHERE user_id=? GROUP BY category", conn, params=(user_id,))
    conn.close()
    return df

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Create tables on first run
create_tables()

# Streamlit app UI
st.title("💰 Expense Tracker")

if not st.session_state.logged_in:
    menu = st.selectbox("Login/Register", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if menu == "Register":
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registered successfully! Please login.")
            else:
                st.error("Username already exists.")
    else:
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
else:
    st.header("Add a New Expense")
    if "date" not in st.session_state:
        st.session_state["date"] = datetime.today().strftime('%Y-%m-%d')
    if "category" not in st.session_state:
        st.session_state["category"] = "Choose an option"
    if "amount" not in st.session_state:
        st.session_state["amount"] = 0.0
    if "description" not in st.session_state:
        st.session_state["description"] = ""
    st.session_state["date"] = st.text_input("Date (YYYY-MM-DD)", st.session_state["date"])
    categories = ["Choose an option", "Food", "Transport", "Shopping", "Bills", "Other"]
    st.session_state["category"] = st.selectbox("Category", categories, index=categories.index(st.session_state["category"]))
    st.session_state["amount"] = st.number_input("Amount", min_value=0.0, format="%.2f", value=st.session_state["amount"])
    st.session_state["description"] = st.text_input("Description", st.session_state["description"])
    if st.button("Add Expense"):
        if st.session_state["date"] and st.session_state["category"] != "Choose an option" and st.session_state["amount"]:
            add_expense(st.session_state["date"], st.session_state["category"], st.session_state["amount"], st.session_state["description"], st.session_state.user_id)
            st.success("Expense added successfully!")
            st.session_state["date"] = datetime.today().strftime('%Y-%m-%d')
            st.session_state["category"] = "Choose an option"
            st.session_state["amount"] = 0.0
            st.session_state["description"] = ""
            st.rerun()
        else:
            st.error("Please fill in all required fields and select a valid category.")
    st.header("📋 Expense List")
    expenses_df = get_expenses(st.session_state.user_id)
    if not expenses_df.empty:
        expenses_df.columns = [col.capitalize() for col in expenses_df.columns]
        st.dataframe(expenses_df)
        selected_id = st.number_input("Enter Expense ID to Delete", min_value=1, step=1)
        if st.button("Delete Expense"):
            delete_expense(selected_id, st.session_state.user_id)
            st.success("Expense deleted successfully!")
            st.rerun()
    else:
        st.info("No expenses recorded yet.")
    st.header("📆 Daily Total Expenses")
    daily_totals = get_daily_total(st.session_state.user_id)
    if not daily_totals.empty:
        daily_totals.columns = [col.capitalize() for col in daily_totals.columns]
        st.dataframe(daily_totals)
    else:
        st.info("No daily expenses recorded yet.")
    st.header("📅 Monthly Total Expenses")
    monthly_totals = get_monthly_total(st.session_state.user_id)
    if not monthly_totals.empty:
        monthly_totals.columns = [col.capitalize() for col in monthly_totals.columns]
        st.dataframe(monthly_totals)
    else:
        st.info("No monthly expenses recorded yet.")
    st.header("📅 Weekly Total Expenses")
    weekly_totals = get_weekly_total(st.session_state.user_id)
    if not weekly_totals.empty:
        weekly_totals.columns = [col.capitalize() for col in weekly_totals.columns]
        st.dataframe(weekly_totals)
    else:
        st.info("No weekly expenses recorded yet.")
    st.header("🔍 Filter Expenses by Category and Date")
    filter_start_date = st.date_input("Select start Date", datetime.today()).strftime('%Y-%m-%d')
    filter_end_date = st.date_input("Select end Date", datetime.today()).strftime('%Y-%m-%d')
    filter_category = st.selectbox("Select Category to Filter", categories[1:])
    if st.button("Filter"):
        filtered_expenses = get_expense_by_date(filter_start_date, st.session_state.user_id)
        if filter_category != "Choose an option":
            filtered_expenses = filtered_expenses[filtered_expenses["category"] == filter_category]
        if not filtered_expenses.empty:
            st.dataframe(filtered_expenses)
        else:
            st.info("No expenses found for the selected category and date.")
    st.header("📊 Expense Report")
    if st.button("Generate Report"):
        report_df = generate_report(st.session_state.user_id)
        if not report_df.empty:
            fig, ax = plt.subplots()
            ax.pie(report_df["total"], labels=report_df["category"], autopct='%1.1f%%', startangle=140)
            ax.set_title("Spending by Category")
            st.pyplot(fig)
        else:
            st.info("No expenses to generate a report.")
