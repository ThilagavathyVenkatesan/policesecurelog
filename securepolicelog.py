import sys
import streamlit as st
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import datetime as dt
import warnings

# ----------------- DB CONFIG -----------------
host = 'localhost'
user = 'root'
password = ''  # Change if needed
database = 'securecheck1'

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# ----------------- LOAD FUNCTIONS -----------------
@st.cache_data
def fetch_data(query):
    try:
        return pd.read_sql(query, con=engine)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

def load_traffic_data():
    try:
        df = pd.read_sql("SELECT * FROM traffic_stops", engine)
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Error loading traffic_stops data: {e}")
        return pd.DataFrame()

# ✅ Load datasets
traffic_data = load_traffic_data()
log_data = fetch_data("SELECT * FROM traffic_stops")

# ----------------- STREAMLIT CONFIG -----------------

st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")
st.title("🚔SecureCheck: Police Check Post Digital Ledger🚔")
st.markdown("🔎Monitor and analyze police stop logs in real time🏢.")


# ----------------- Police Logs Display -----------------
st.header("👮Police Logs Overview👮")
st.dataframe(log_data, use_container_width=True)

# ----------------- METRICS -----------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Police Stops", len(traffic_data))

with col2:
    if 'stop_outcome' in traffic_data.columns:
        arrests = traffic_data[traffic_data['stop_outcome'].str.contains("arrest", case=False, na=False)].shape[0]
        st.metric("Total Arrests", arrests)
    else:
        st.warning("'stop_outcome' column not found")

with col3:
    if 'stop_outcome' in traffic_data.columns:
        warnings = traffic_data[traffic_data['stop_outcome'].str.contains("warning", case=False, na=False)].shape[0]
        st.metric("Total Warnings", warnings)
    else:
        st.warning("'stop_outcome' column not found")

with col4:
    if 'drugs_related_stop' in traffic_data.columns:
        drug_stops = traffic_data[traffic_data['drugs_related_stop'].astype(str).str.lower().isin(['true', '1'])].shape[0]
        st.metric("Drug Related Stops", drug_stops)
    else:
        st.warning("'drugs_related_stop' column not found")

# Charts
st.header("📈 Visual Insights")

tab1, tab2 = st.tabs(["Stops by Violation", "Driver Gender Distribution"])

with tab1:
    if not traffic_data.empty and 'violation' in traffic_data.columns:
        violation_data = traffic_data['violation'].value_counts().reset_index()
        violation_data.columns = ['Violation', 'Count']
        fig = px.bar(violation_data, x='Violation', y='Count', title="Stops by Violation Type", color='Violation')
        st.plotly_chart(fig, use_container_width=True)
        # ✅ Add checkbox to show raw data
        if st.checkbox("Show raw violation counts (table)"):
            st.subheader("📋 Violation Count Table (Raw)")
            st.dataframe(violation_data)
    else:
        st.warning("No data available for Violation chart.")

with tab2:
    if not traffic_data.empty and 'driver_gender' in traffic_data.columns:
        gender_data = traffic_data['driver_gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        fig = px.pie(gender_data, names='Gender', values='Count', title="Driver Gender Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Driver Gender chart.")


# ------------------ QUERY ANALYTICS SECTION ------------------

st.markdown("## 🔍 Query Analytics")

# Medium Query Map (unchanged from your code)
st.header("Medium Level Queries")
with st.expander("🟠 Medium Level Queries", expanded=True):
    medium_query_map = {
        "Top 10 vehicle_Number involved in drug-related stops": """
            SELECT vehicle_number, COUNT(*) AS stop_count
            FROM traffic_stops
            WHERE drugs_related_stop = 1
            GROUP BY vehicle_number
            ORDER BY stop_count DESC
            LIMIT 10
        """,

        "Vehicles most frequently searched": """
            SELECT vehicle_number, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY vehicle_number
            ORDER BY search_count DESC
            LIMIT 10
        """,

        "Age group of the driver had the highest arrest rate": """
            SELECT driver_age, COUNT(*) AS arrest_count
            FROM traffic_stops
            WHERE stop_outcome LIKE '%%arrest%%'
            GROUP BY driver_age
            ORDER BY arrest_count DESC
            LIMIT 1
        """,

        "Gender distribution of drivers stopped in each country": """
            SELECT country_name, driver_gender, COUNT(*) AS total
            FROM traffic_stops
            GROUP BY country_name, driver_gender
            ORDER BY country_name, driver_gender
        """,

        "Highest search rate of Race and Gender combination": """
            SELECT driver_race, driver_gender, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY driver_race, driver_gender
            ORDER BY search_count DESC
            LIMIT 1
        """,

        "Time of day the most traffic stops": """
            SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS stop_count
            FROM traffic_stops
            GROUP BY hour_of_day
            ORDER BY stop_count DESC
            LIMIT 1
        """,

        "Average stop duration for different violations": """
            SELECT violation, AVG(
                CASE 
                    WHEN stop_duration = '0-15 Min' THEN 7.5
                    WHEN stop_duration = '16-30 Min' THEN 23
                    WHEN stop_duration = '30+ Min' THEN 40
                    ELSE 15
                END
            ) AS avg_duration_minutes
            FROM traffic_stops
            GROUP BY violation
            ORDER BY avg_duration_minutes DESC
        """,

        "Stops during the night more likely to lead to arrests": """
            SELECT COUNT(*) AS arrest_count
            FROM traffic_stops
            WHERE (HOUR(stop_time) >= 20 OR HOUR(stop_time) <= 5)
            AND stop_outcome LIKE '%%arrest%%'
        """,

        "Most Violations associated with searches or arrests": """
            SELECT violation, COUNT(*) AS incident_count
            FROM traffic_stops
            WHERE search_conducted = 1 OR stop_outcome LIKE '%%arrest%%'
            GROUP BY violation
            ORDER BY incident_count DESC
        """,

        "Most violations common among younger drivers (<25)": """
            SELECT violation, COUNT(*) AS violation_count
            FROM traffic_stops
            WHERE driver_age < 25
            GROUP BY violation
            ORDER BY violation_count DESC
        """,

        "Violation that rarely results in search or arrest": """
            SELECT violation, COUNT(*) AS count
            FROM traffic_stops
            WHERE search_conducted = 0 AND stop_outcome NOT LIKE '%%arrest%%'
            GROUP BY violation
            ORDER BY count ASC
            LIMIT 1
        """,

        "Countries report the highest rate of drug-related stops": """
            SELECT country_name, COUNT(*) AS drug_stop_count
            FROM traffic_stops
            WHERE drugs_related_stop = 1
            GROUP BY country_name
            ORDER BY drug_stop_count DESC
        """,

        "The most stops with search conducted in country": """
            SELECT country_name, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = 1
            GROUP BY country_name
            ORDER BY search_count DESC
            LIMIT 1
        """
    }
selected_medium = st.selectbox("🔸 Select a Medium Level Query", list(medium_query_map.keys()))
if st.button("🔘Run Medium Query"):
    query = medium_query_map[selected_medium]
    result = fetch_data(query)
    if not result.empty:
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("No results returned for this query.")

# ----------------- COMPLEX QUERIES -----------------
st.header("Complex Level Queries")
with st.expander("🔵 Complex Level Queries", expanded=False):
    complex_query_map = {
        "Yearly Breakdown of Stops and Arrests by Country": """
            SELECT
                country_name,
                YEAR(stop_date) AS stop_year,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(100.0 * SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY country_name, stop_year
            ORDER BY country_name, stop_year
        """,

        "Driver Violation Trends Based on Age and Race": """
            SELECT
                driver_race,
                CASE 
                    WHEN driver_age < 25 THEN '<25'
                    WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
                    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+'
                END AS age_group,
                violation,
                COUNT(*) AS count
            FROM traffic_stops
            GROUP BY driver_race, age_group, violation
            ORDER BY driver_race, age_group, count DESC
        """,

        "Time Period Analysis of Stops": """
            SELECT
                YEAR(stop_date) AS year,
                MONTH(stop_date) AS month,
                HOUR(stop_time) AS hour,
                COUNT(*) AS stop_count
            FROM traffic_stops
            GROUP BY year, month, hour
            ORDER BY year, month, hour
        """,

        "Violations with High Search and Arrest Rates": """
            SELECT
                violation,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) AS total_searches,
                SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(100.0 * SUM(CASE WHEN search_conducted = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate,
                ROUND(100.0 * SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            HAVING total_stops > 10
            ORDER BY arrest_rate DESC
        """,

        "Driver Demographics by Country": """
            SELECT
                country_name,
                driver_gender,
                driver_race,
                AVG(driver_age) AS avg_age,
                COUNT(*) AS total_stops
            FROM traffic_stops
            GROUP BY country_name, driver_gender, driver_race
            ORDER BY country_name, total_stops DESC
        """,

        "Top 5 Violations with Highest Arrest Rates": """
            SELECT
                violation,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) AS arrest_count,
                ROUND(100.0 * SUM(CASE WHEN stop_outcome LIKE '%%arrest%%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            HAVING total_stops > 10
            ORDER BY arrest_rate DESC
            LIMIT 5
        """
    }

selected_complex = st.selectbox("🔹 Select a Complex Level Query", list(complex_query_map.keys()))
if st.button("🔘Run Complex Query"):
    query = complex_query_map[selected_complex]
    result = fetch_data(query)
    if not result.empty:
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("No results returned for this query.")

# ----------------- PREDICT STOP OUTCOME -----------------
st.markdown("---")
st.header("Add New Police Log & Predict Outcome and Violation")

with st.form("new_log_form"):
    stop_date = st.date_input("Stop Date")
    stop_time = st.time_input("Stop Time")
    country_name = st.text_input("Country Name")
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=27)
    driver_race = st.text_input("Driver Race")
    search_conducted = st.selectbox("Is a Search Conducted?", ["0", "1"])
    search_type = st.text_input("Search Type")
    drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
    stop_duration = st.selectbox("Stop Duration", traffic_data["stop_duration"].dropna().unique())
    vehicle_number = st.text_input("Vehicle Number")
    submitted = st.form_submit_button("Predict Stop Outcome & Violation")

if submitted:
    filtered_data = traffic_data[
        (traffic_data["driver_gender"] == driver_gender) &
        (traffic_data["driver_age"] == driver_age) &
        (traffic_data["search_conducted"] == int(search_conducted)) &
        (traffic_data["stop_duration"] == stop_duration) &
        (traffic_data["drugs_related_stop"] == int(drugs_related_stop))
    ]

    predicted_outcome = filtered_data["stop_outcome"].mode()[0] if not filtered_data.empty else "Warning"
    predicted_violation = filtered_data["violation"].mode()[0] if not filtered_data.empty else "Speeding"

    st.markdown("### Prediction Summary")
    st.markdown(f"**Predicted Violation:** {predicted_violation}")
    st.markdown(f"**Predicted Stop Outcome:** {predicted_outcome}")

    search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
    drug_text = "was drug-related" if int(drugs_related_stop) else "was not drug-related"

    st.markdown(f"""
        A {driver_age}-year-old {driver_gender} driver in **{country_name}** was stopped at **{stop_time.strftime('%I:%M %p')}** on **{stop_date}**.  
        {search_text} and the stop {drug_text}.  
        **Stop Duration**: {stop_duration}  
        **Vehicle Number**: {vehicle_number}
    """)

# ----------------- Footer -----------------
st.markdown("---")
st.markdown("Built with ❤️ for Law Enforcement by SecureCheck")
