import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from add_update_ui import add_update_tab
from analytics_category_ui import analytics_category_tab
from analytics_months_ui import analytics_months_tab

API_url = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Expense Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome-text {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #200eaa 0%, #600ba2 100%);
        padding: 10px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px;
        width: 100%;
    }
    .stButton>button {
        background: linear-gradient(135deg, #200eaa 0%, #650ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Session states
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

# ------------------------
# SIDEBAR - LOGIN / REGISTER
# ------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: white;'>💰 Expense Manager</h1>
        <p style='color: white;'>Track your expenses effortlessly</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.user is None:
        st.markdown("---")
        choice = st.selectbox("**Select Action**", ["Login", "Create User"],
                              help="Choose to login or create new account")
        username = st.text_input("**Username**", placeholder="Enter your username")
        password = st.text_input("**Password**", type="password", placeholder="Enter your password")

        if choice == "Login" and st.button("🚀 Login", use_container_width=True):
            with st.spinner("Logging in..."):
                login_response = requests.post(f"{API_url}/login/", json={"username": username, "password": password})
                if login_response.status_code == 200:
                    data = login_response.json()
                    st.session_state.user = username
                    st.session_state.token = data["access_token"]
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif choice == "Create User" and st.button("✨ Create Account", use_container_width=True):
            with st.spinner("Creating account..."):
                create_response = requests.post(f"{API_url}/create_user/", json={"username": username, "password": password})
                if create_response.status_code == 200:
                    st.success("✅ Account created successfully! Please login.")
                else:
                    st.error("❌ Username already exists")
    else:
        st.markdown("---")
        st.markdown(f"### 👋 Welcome, **{st.session_state.user}**")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.token = None
            st.rerun()

# ------------------------
# MAIN CONTENT AREA
# ------------------------
if st.session_state.user is None:
    # Landing page when not logged in
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>💰 Expense Manager</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='welcome-text'>Track your expenses, analyze spending patterns, and take control of your finances</p>",
            unsafe_allow_html=True)

        # Features grid
        col11, col12, col13 = st.columns(3)
        with col11:
            st.markdown("""
            <div class='metric-card'>
                <h3>📊 Analytics</h3>
                <p>Visualize your spending patterns</p>
            </div>
            """, unsafe_allow_html=True)
        with col12:
            st.markdown("""
            <div class='metric-card'>
                <h3>📅 Daily Tracking</h3>
                <p>Log expenses effortlessly</p>
            </div>
            """, unsafe_allow_html=True)
        with col13:
            st.markdown("""
            <div class='metric-card'>
                <h3>📈 Insights</h3>
                <p>Get valuable financial insights</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.info("👈 Please login or create an account from the sidebar to get started!")

else:
        # Main dashboard when logged in
        st.markdown(f"<h1 class='main-header'>Welcome back, {st.session_state.user}! 👋</h1>", unsafe_allow_html=True)

        # Quick stats at the top
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        today = datetime.now().date()

        try:
            # Get today's expenses for quick stats
            today_response = requests.get(f"{API_url}/expenses/?expense_date={today}", headers=headers)
            if today_response.status_code == 200:
                expenses = today_response.json()
                total_today = sum(expense['amount'] for expense in expenses) if expenses else 0

                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>💰 Today's Total</h3>
                        <h2>INR {total_today:.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>📊 Expenses Today</h3>
                        <h2>{len(expenses)}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>📅 Date</h3>
                        <h4>{today.strftime('%b %d, %Y')}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h3>👤 User</h3>
                        <h4>{st.session_state.user}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading today's expenses: {str(e)}")

        st.markdown("---")

        # Tabs with modern styling
        tab1, tab2, tab3 = st.tabs(['📝 Add/Update Expenses', '📊 Category Analytics', '📅 Monthly Trends'])

        with tab1:
            add_update_tab()

        with tab2:
            analytics_category_tab()

        with tab3:
            analytics_months_tab()

        st.markdown("---")

        # ... (previous code remains the same)

        # Today's expenses section
        st.subheader("📋Today's Expenses")
        expense_date = st.date_input("Select Date", value=datetime.now().date(), key="date_selector")

        try:
            expenses_response = requests.get(f"{API_url}/expenses/?expense_date={expense_date}", headers=headers)
            if expenses_response.status_code == 200:
                expenses_data = expenses_response.json()

                # Debug: Check what fields we actually get
                #st.write("🔍 Debug - Expense data fields:", expenses_data[0].keys() if expenses_data else "No data")

                if expenses_data:
                    df = pd.DataFrame(expenses_data)

                    # Check what date field name we have and handle accordingly
                    date_column = None
                    possible_date_columns = ['expense_date', 'date', 'expenseDate', 'expense_date']

                    for col in possible_date_columns:
                        if col in df.columns:
                            date_column = col
                            break

                    # Format the display
                    df_display = df.copy()
                    df_display['amount'] = df_display['amount'].apply(lambda x: f"INR {x:.2f}")

                    if date_column:
                        try:
                            df_display['date'] = pd.to_datetime(df_display[date_column]).dt.strftime('%b %d, %Y')
                            display_columns = ['date', 'category', 'amount', 'notes']
                        except:
                            df_display['date'] = df_display[date_column].astype(str)
                            display_columns = ['date', 'category', 'amount', 'notes']
                    else:
                        display_columns = ['category', 'amount', 'notes']

                    st.dataframe(
                        df_display[display_columns],
                        use_container_width=True,
                        hide_index=True
                    )

                    # Quick pie chart
                    if len(expenses_data) > 0:
                        fig = px.pie(
                            df,
                            values='amount',
                            names='category',
                            title=f'Expense Distribution for {expense_date.strftime("%b %d, %Y")}',
                            color_discrete_sequence=px.colors.sequential.RdBu
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No expenses recorded for this date. Add some expenses in the Add/Update tab!")
            else:
                st.error(f"Failed to fetch expenses: {expenses_response.status_code}")
        except Exception as e:
            st.error(f"Error loading expenses: {str(e)}")
            # Show the actual data for debugging
            if 'expenses_data' in locals():
                st.write("Actual data received:", expenses_data)