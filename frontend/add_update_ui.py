import streamlit as st
import requests
from datetime import datetime

API_url = "http://localhost:8000"


def add_update_tab():
    selected_date = st.date_input("Date", datetime.now().date(), label_visibility="collapsed")

    # Get expenses with authentication
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(
        f"{API_url}/expenses/?expense_date={selected_date}",
        headers=headers
    )

    expenses = []
    if response.status_code == 200:
        expenses = response.json()
    else:
        st.error(f"Failed to fetch expenses: {response.status_code}")

    categories = ['Rent', 'Entertainment', 'Food', 'Shopping', 'Other']

    with st.form(key='expense_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        expense_inputs = []
        for i in range(5):
            if i < len(expenses):
                amount = expenses[i]["amount"]
                category = expenses[i]["category"]
                notes = expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    value=float(amount),
                    step=1.0,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category) if category in categories else 0,
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expense_inputs.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit = st.form_submit_button(label="Submit")
        if submit:
            # Filter out expenses with amount 0
            filtered_expenses = [expense for expense in expense_inputs if expense['amount'] > 0]

            # Send request with authentication
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(
                f"{API_url}/expenses/?expense_date={selected_date}",
                json=filtered_expenses,
                headers=headers
            )

            if response.status_code == 200:
                st.success('Expense updated successfully')
                st.rerun()  # Refresh the page
            else:
                st.error(f'Failed to update expense: {response.status_code}')