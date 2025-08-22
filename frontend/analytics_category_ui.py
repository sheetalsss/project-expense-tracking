import pandas as pd
import streamlit as st
import requests
from datetime import datetime
import json

API_url = "http://localhost:8000"


def analytics_category_tab():
    st.header("📊 Category Analytics")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if st.button("Get Analytics"):
        # First, check if user is authenticated
        if not st.session_state.token:
            st.error("Please login first!")
            return

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            response = requests.post(f"{API_url}/analytics/", json=payload, headers=headers)

            # Debug information
            #st.write(f"🔍 Status Code: {response.status_code}")

            # Check if response is successful
            if response.status_code != 200:
                st.error(f"❌ API Error: {response.status_code}")
              #  st.write(f"Error message: {response.text}")
                return

            # Try to parse JSON response
            try:
                response_data = response.json()
               # st.write(f"🔍 Response Type: {type(response_data)}")
                #st.write(f"🔍 Response Content: {response_data}")

            except json.JSONDecodeError:
                st.error("❌ Failed to parse JSON response from server")
               # st.write(f"Raw response: {response.text}")
                return

            # Handle different response formats
            if isinstance(response_data, str):
                # Server returned a string error message
                st.error(f"❌ Server Error: {response_data}")
                return

            elif isinstance(response_data, dict) and "detail" in response_data:
                # Server returned an error dictionary
                st.error(f"❌ Error: {response_data['detail']}")
                return

            elif not response_data:
                # Empty response
                st.info("ℹ️ No expense data available for the selected date range")
                return

            elif isinstance(response_data, dict):
                # This is the expected format - process the data
                try:
                    print(response_data)
                    response_data = dict(response_data)
                    data = {
                        "Category": list(response_data.keys()),
                        "Total": [response_data[category]['total'] for category in response_data],
                        "Percentage": [response_data[category]['percentage'] for category in response_data]
                    }

                    df = pd.DataFrame(data)
                    df_sorted = df.sort_values(by="Percentage", ascending=False)

                    st.title("Expense Breakdown by Category")
                    st.bar_chart(data=df_sorted.set_index('Category')['Percentage'])
                    st.table(df_sorted)

                except KeyError as e:
                    st.error(f"❌ Data format error: Missing key {e}")
                   # st.write("Received data structure:", response_data)
                except Exception as e:
                    st.error(f"❌ Error processing data: {str(e)}")
                 #   st.write("Raw data:", response_data)

            else:
                st.error(f"❌ Unexpected response format: {type(response_data)}")
               # st.write("Received:", response_data)

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the server. Please make sure the backend is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")