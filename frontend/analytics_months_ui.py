import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

API_url = "http://localhost:8000"


def analytics_months_tab():
    st.header("📅 Monthly Trends")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    with st.spinner("Loading monthly data..."):
        try:
            response = requests.get(f"{API_url}/analytics_by_month/", headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data and isinstance(data, list):
                    df = pd.DataFrame(data)

                    # Create month names mapping
                    month_map = {
                        '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
                        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
                        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
                    }

                    # Extract year and month for better display
                    df['Year'] = df['month_year'].str[:4]
                    df['Month'] = df['month_year'].str[5:7].map(month_map)
                    df['Year-Month'] = df['Month'] + ' ' + df['Year']

                    # Display metrics
                    total_months = len(df)
                    avg_monthly = df['total_amount'].mean()
                    max_month = df.loc[df['total_amount'].idxmax()]

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📅 Months Tracked", total_months)
                    with col2:
                        st.metric("💰 Avg Monthly", f"INR {avg_monthly:.2f}")
                    with col3:
                        st.metric("📈 Highest Month", f"INR {max_month['total_amount']:.2f}")

                    # Create visualizations
                    fig = px.line(
                        df,
                        x='Year-Month',
                        y='total_amount',
                        title='Monthly Expense Trends',
                        markers=True,
                        labels={'total_amount': 'Total Amount', 'Year-Month': 'Month'}
                    )
                    fig.update_traces(line=dict(color='#FF4B4B', width=3))
                    st.plotly_chart(fig, use_container_width=True)

                    # Bar chart
                    fig2 = px.bar(
                        df,
                        x='Year-Month',
                        y='total_amount',
                        title='Monthly Expenses',
                        color='total_amount',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                    # Display table
                    st.subheader("📋 Monthly Summary")
                    display_df = df[['Year-Month', 'total_amount']].copy()
                    display_df['total_amount'] = display_df['total_amount'].apply(lambda x: f"INR {x:.2f}")
                    display_df.columns = ['Month', 'Total Amount']
                    st.dataframe(display_df, use_container_width=True, hide_index=True)

                else:
                    st.info("No monthly data available yet. Start adding expenses to see trends!")

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Error loading monthly data: {str(e)}")