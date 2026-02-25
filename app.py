import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ola Ride Insights", layout="wide")

st.title("🚖 Ola Ride Insights Dashboard")
st.markdown("Interactive Analytics Dashboard for Ride Sharing Data")

# Load Data
@st.cache
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")

vehicle = st.sidebar.multiselect(
    "Select Vehicle Type",
    options=df["vehicle_type"].unique(),
    default=df["vehicle_type"].unique()
)

status = st.sidebar.multiselect(
    "Select Booking Status",
    options=df["booking_status"].unique(),
    default=df["booking_status"].unique()
)

filtered_df = df[
    (df["vehicle_type"].isin(vehicle)) &
    (df["booking_status"].isin(status))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Rides", len(filtered_df))
col2.metric("Total Revenue", f"₹ {filtered_df['booking_value'].sum():,.0f}")
col3.metric("Avg Distance", f"{filtered_df['ride_distance'].mean():.2f} km")
col4.metric("Avg Rating", f"{filtered_df['customer_rating'].mean():.2f}")

st.markdown("---")
st.header("📊 Power BI Dashboard Views")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚖 Overall")
    st.image("powerbi_overall.png.png", use_column_width=True)

with col2:
    st.subheader("💰 Revenue")
    st.image("powerbi_revenue.png.png", use_column_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("❌ Cancellation")
    st.image("powerbi_cancellation.png.png", use_column_width=True)

with col4:
    st.subheader("⭐ Rating")
    st.image("powerbi_ratings.png.png", use_column_width=True)

# Row 3
st.subheader("🚘 Vehicle Type Analysis")
st.image("powerbi_vehicle_type.png.png", use_column_width=True)

st.markdown("---")

# Ride Volume Over Time
st.subheader("📈 Ride Volume Over Time")
ride_time = filtered_df.groupby("date").size().reset_index(name="Ride Count")
fig1 = px.line(ride_time, x="date", y="Ride Count")
st.plotly_chart(fig1, use_container_width=True)

# Booking Status Breakdown
st.subheader("📊 Booking Status Breakdown")
fig2 = px.pie(filtered_df, names="booking_status")
st.plotly_chart(fig2, use_container_width=True)

# Revenue by Payment Method
st.subheader("💰 Revenue by Payment Method")
revenue_payment = filtered_df.groupby("payment_method")["booking_value"].sum().reset_index()
fig3 = px.bar(revenue_payment, x="payment_method", y="booking_value")
st.plotly_chart(fig3, use_container_width=True)

# Top 5 Customers
st.subheader("🏆 Top 5 Customers by Booking Value")
top_customers = filtered_df.groupby("customer_id")["booking_value"].sum().reset_index()
top_customers = top_customers.sort_values(by="booking_value", ascending=False).head(5)
st.dataframe(top_customers)

# Ratings Distribution
st.subheader("⭐ Driver Ratings Distribution")
fig4 = px.histogram(filtered_df, x="driver_rating", nbins=10)
st.plotly_chart(fig4, use_container_width=True)

st.success("Dashboard Loaded Successfully 🚀")


