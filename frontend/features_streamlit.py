import streamlit as st
from datetime import datetime
import requests
import pandas as pd

from add_update_ui import add_update_tab
from analytics_category_ui import analytics_category_tab
from analytics_months_ui import analytics_months_tab

API_url = "http://localhost:8000"

st.title("Expense Management System")

# Session states
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# ------------------------
# LOGIN / REGISTER SCREEN
# ------------------------
if st.session_state.user is None:
    choice = st.selectbox("Select an action", ["Login", "Create User"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login" and st.button("Login"):
        response = requests.post(f"{API_url}/login/", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state.user = username
            st.session_state.token = data["access_token"]   # assuming JWT from backend
            st.success(f"Logged in as {username}")
            st.rerun()  # Changed from experimental_rerun() to rerun()
        else:
            st.error("Invalid credentials")

    elif choice == "Create User" and st.button("Create User"):
        response = requests.post(f"{API_url}/create_user/", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("User created successfully, please login.")
        else:
            st.error("Username already exists")

# ------------------------
# MAIN APP AFTER LOGIN
# ------------------------
else:
    print(st.session_state.user)
    st.write(f"Welcome, {st.session_state.user} 👋")
    expense_date = st.date_input("Expense Date", value=datetime.now().date())

    # Tabs
    tab1, tab2, tab3 = st.tabs(['Add/Update', 'Analytics by Category', 'Analytics by Months'])

    with tab1:
        add_update_tab()
    with tab2:
        analytics_category_tab()
    with tab3:
        analytics_months_tab()

    # Fetch expenses (with auth header)
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_url}/expenses?date={expense_date}", headers=headers)

    if response.status_code == 200:
        expenses = response.json()
        if expenses:
            st.table(pd.DataFrame(expenses))
        else:
            st.info("No expenses recorded for this date.")
    else:
        st.error("Failed to fetch expenses")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()  # Changed from experimental_rerun() to rerun()