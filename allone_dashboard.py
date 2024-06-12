import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# Connect to the SQLite database
conn = sqlite3.connect("allone\data\all_one_inc.db")

# Load the cleaned data from the SQLite database
query = "SELECT * FROM all_one_sales"  # Adjust the table name if necessary
sales_data = pd.read_sql(query, conn)

# Convert Date column to datetime
sales_data['Date'] = pd.to_datetime(sales_data['Date'])

# Add a 'Year' column by extracting the year from the 'Date' column
sales_data['Year'] = sales_data['Date'].dt.year

# Rename columns to remove spaces
sales_data = sales_data.rename(columns={"Period No": "Period_No"})

# Calculate the most recent year
most_recent_year = sales_data["Year"].max()

# Sidebar filters
selected_years = st.sidebar.multiselect(
    "Select Year:",
    options=sales_data["Year"].unique().tolist(),
    default=[most_recent_year]
)

# Add "Select All" option for dates
all_dates = sales_data["Date"].dt.strftime('%Y-%m-%d').unique().tolist()
all_dates.insert(0, "Select All")

# Sort the dates in descending order (except "Select All")
all_dates[1:] = sorted(all_dates[1:], key=lambda x: pd.to_datetime(x), reverse=True)

# Calculate the most recent date
most_recent_date = sales_data["Date"].max().strftime('%Y-%m-%d')

# Set the default value for the selectbox to the most recent date
selected_date = st.sidebar.selectbox("Select Date:", options=all_dates, index=all_dates.index(most_recent_date) + 1)

# Handle "Select All" option for dates
if selected_date == "Select All":
    selected_dates = sales_data["Date"].dt.strftime('%Y-%m-%d').unique().tolist()
else:
    selected_dates = [selected_date]

# Add "Select All" option for periods
all_periods = sales_data["Period_No"].unique().tolist()
all_periods.insert(0, "Select All")

selected_period = st.sidebar.selectbox("Select Period:", options=all_periods)

# Handle "Select All" option for periods
if selected_period == "Select All":
    selected_periods = sales_data["Period_No"].unique().tolist()
else:
    selected_periods = [selected_period]

selected_stores = st.sidebar.multiselect("Select Store:", options=sales_data["Store"].unique().tolist(), default=sales_data['Store'].unique().tolist())

# Add a checkbox to toggle the display of the DataFrame
show_dataframe = st.sidebar.checkbox("Show Sales Data")

# Filter the data based on sidebar inputs
filtered_sales_data = sales_data[
    (sales_data['Year'].isin(selected_years)) &
    (sales_data['Date'].dt.strftime('%Y-%m-%d').isin(selected_dates)) &
    (sales_data['Period_No'].isin(selected_periods)) &
    (sales_data['Store'].isin(selected_stores))
]

# Sort the filtered data by Date in descending order
filtered_sales_data = filtered_sales_data.sort_values(by='Date', ascending=False)

# Streamlit app
def main():
    st.title(":bar_chart: Sales Data Dashboard")
    st.markdown('##')

    # Create two columns
    col1, col2 = st.columns(2)

    # Display filtered data
    # st.write("Filtered Sales Data", filtered_sales_data)

    # Calculate metrics
    with col1:
        if not filtered_sales_data.empty:
            total_sales = int(filtered_sales_data['Total Revenue'].sum())
            average_ticket = filtered_sales_data['Avg Ticket'].mean()
            customer_count = filtered_sales_data['Cust Count'].sum()
            labor = filtered_sales_data['Labor %'].mean()
            food = filtered_sales_data['Food %'].mean()

            st.subheader(f"Total Sales: ${total_sales:,.2f}")
            aggregated_data = filtered_sales_data.groupby('Date')['Total Revenue'].sum().reset_index()
            fig_total_sales = px.line(aggregated_data, x='Date', y='Total Revenue', title="Total Sales", color_discrete_sequence=["#0083B8"] * len(aggregated_data), template="plotly_white")
            st.plotly_chart(fig_total_sales)

            st.subheader(f"Average Ticket: ${average_ticket:.2f}")
            aggregated_data1 = filtered_sales_data.groupby('Date')['Avg Ticket'].mean().reset_index()
            fig_average_ticket = px.line(aggregated_data1, x='Date', y='Avg Ticket', title='Average Ticket')
            st.plotly_chart(fig_average_ticket)

            st.subheader(f"Food %: {food:.2f}")
            aggregated_data4 = filtered_sales_data.groupby('Date')['Food %'].mean().reset_index()
            fig_food = px.line(aggregated_data4, x='Date', y='Food %', title='Food %')
            st.plotly_chart(fig_food)

    with col2:
        if not filtered_sales_data.empty:
            st.subheader(f"Customer Count: {customer_count:,.0f}")
            aggregated_data3 = filtered_sales_data.groupby('Date')['Cust Count'].sum().reset_index()
            fig_cust_count = px.bar(aggregated_data3, x='Date', y='Cust Count', title='Customer Count')
            st.plotly_chart(fig_cust_count)

            st.subheader(f"Labor %: {labor:.2f}")
            aggregated_data2 = filtered_sales_data.groupby('Date')['Labor %'].mean().reset_index()
            fig_labor = px.bar(aggregated_data2, x='Date', y='Labor %', title='Labor %')
            st.plotly_chart(fig_labor)
        else:
            st.write("No data available for the selected filters.")

    if show_dataframe:
        st.write("Sales Data", filtered_sales_data)

if __name__ == "__main__":
    main()
