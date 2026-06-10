
# ============================================================
# Task 5: Interactive Business Dashboard in Streamlit
# Dataset: Global Superstore Dataset
# Objective: Analyze sales, profit, and segment-wise performance
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Global Superstore Business Dashboard",
    page_icon="📊",
    layout="wide"
)


# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

@st.cache_data
def load_data():
    """
    Load the Global Superstore dataset.
    The CSV file should be placed in the same folder as app.py.
    """

    df = pd.read_csv("Global_Superstore.csv", encoding="latin1")
    return df


# ------------------------------------------------------------
# Clean Dataset
# ------------------------------------------------------------

def clean_data(df):
    """
    Clean and prepare the Global Superstore dataset.
    """

    df = df.copy()

    # Clean column names
    df.columns = df.columns.str.strip()

    df.columns = (
        df.columns
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.lower()
    )

    # Convert date columns
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    if "ship_date" in df.columns:
        df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    # Convert numeric columns
    numeric_columns = [
        "sales",
        "profit",
        "quantity",
        "discount",
        "shipping_cost"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop duplicate records
    df = df.drop_duplicates()

    # Drop rows with missing critical values
    critical_columns = [
        "sales",
        "profit",
        "region",
        "category",
        "sub_category"
    ]

    existing_critical_columns = [
        col for col in critical_columns if col in df.columns
    ]

    df = df.dropna(subset=existing_critical_columns)

    # Handle missing customer names
    if "customer_name" in df.columns:
        df["customer_name"] = df["customer_name"].fillna("Unknown Customer")

    # Create time-based columns
    if "order_date" in df.columns:
        df["year"] = df["order_date"].dt.year
        df["month"] = df["order_date"].dt.month
        df["month_name"] = df["order_date"].dt.month_name()
        df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

    # Create profit margin
    if "sales" in df.columns and "profit" in df.columns:
        df["profit_margin"] = (df["profit"] / df["sales"]) * 100
        df["profit_margin"] = df["profit_margin"].replace(
            [float("inf"), float("-inf")],
            0
        )
        df["profit_margin"] = df["profit_margin"].fillna(0)

    return df


# ------------------------------------------------------------
# Apply Dashboard Filters
# ------------------------------------------------------------

def apply_filters(df, selected_regions, selected_categories, selected_subcategories):
    """
    Filter the dataframe based on sidebar selections.
    """

    filtered_df = df.copy()

    if selected_regions:
        filtered_df = filtered_df[
            filtered_df["region"].isin(selected_regions)
        ]

    if selected_categories:
        filtered_df = filtered_df[
            filtered_df["category"].isin(selected_categories)
        ]

    if selected_subcategories:
        filtered_df = filtered_df[
            filtered_df["sub_category"].isin(selected_subcategories)
        ]

    return filtered_df


# ------------------------------------------------------------
# Dashboard Header
# ------------------------------------------------------------

st.title("Global Superstore Business Dashboard")

st.markdown(
    """
    This interactive dashboard analyzes sales, profit, customer performance,
    and product-level performance using the Global Superstore Dataset.
    """
)


# ------------------------------------------------------------
# Load and Clean Data
# ------------------------------------------------------------

try:
    raw_df = load_data()
    df = clean_data(raw_df)

except Exception as error:
    st.error("Dataset could not be loaded. Make sure Global_Superstore.csv exists in the same folder as app.py.")
    st.stop()


# ------------------------------------------------------------
# Sidebar Filters
# ------------------------------------------------------------

st.sidebar.header("Dashboard Filters")

regions = sorted(df["region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

categories = sorted(df["category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)

subcategories = sorted(df["sub_category"].dropna().unique())
selected_subcategories = st.sidebar.multiselect(
    "Select Sub-Category",
    options=subcategories,
    default=subcategories
)

filtered_df = apply_filters(
    df,
    selected_regions,
    selected_categories,
    selected_subcategories
)


# ------------------------------------------------------------
# Empty Data Handling
# ------------------------------------------------------------

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ------------------------------------------------------------
# KPI Section
# ------------------------------------------------------------

st.subheader("Key Performance Indicators")

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()

if "order_id" in filtered_df.columns:
    total_orders = filtered_df["order_id"].nunique()
else:
    total_orders = len(filtered_df)

average_profit_margin = filtered_df["profit_margin"].mean()

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)

kpi_1.metric("Total Sales", f"${total_sales:,.0f}")
kpi_2.metric("Total Profit", f"${total_profit:,.0f}")
kpi_3.metric("Total Orders", f"{total_orders:,}")
kpi_4.metric("Average Profit Margin", f"{average_profit_margin:.2f}%")


# ------------------------------------------------------------
# Sales by Region
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Sales and Profit Analysis")

sales_by_region = (
    filtered_df
    .groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values(by="sales", ascending=False)
)

fig_sales_region = px.bar(
    sales_by_region,
    x="region",
    y="sales",
    title="Total Sales by Region",
    text_auto=".2s"
)

fig_sales_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Sales"
)

st.plotly_chart(fig_sales_region, use_container_width=True)


# ------------------------------------------------------------
# Profit by Category and Sales by Segment
# ------------------------------------------------------------

chart_col_1, chart_col_2 = st.columns(2)

with chart_col_1:
    profit_by_category = (
        filtered_df
        .groupby("category", as_index=False)["profit"]
        .sum()
        .sort_values(by="profit", ascending=False)
    )

    fig_profit_category = px.bar(
        profit_by_category,
        x="category",
        y="profit",
        title="Profit by Category",
        text_auto=".2s"
    )

    fig_profit_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Profit"
    )

    st.plotly_chart(fig_profit_category, use_container_width=True)

with chart_col_2:
    if "segment" in filtered_df.columns:
        sales_by_segment = (
            filtered_df
            .groupby("segment", as_index=False)["sales"]
            .sum()
            .sort_values(by="sales", ascending=False)
        )

        fig_sales_segment = px.pie(
            sales_by_segment,
            names="segment",
            values="sales",
            title="Sales Share by Segment"
        )

        st.plotly_chart(fig_sales_segment, use_container_width=True)
    else:
        st.info("Segment column is not available in this dataset.")


# ------------------------------------------------------------
# Top 5 Customers by Sales
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Top 5 Customers by Sales")

if "customer_name" in filtered_df.columns:
    top_customers = (
        filtered_df
        .groupby("customer_name", as_index=False)["sales"]
        .sum()
        .sort_values(by="sales", ascending=False)
        .head(5)
    )

    fig_top_customers = px.bar(
        top_customers,
        x="sales",
        y="customer_name",
        orientation="h",
        title="Top 5 Customers by Sales",
        text_auto=".2s"
    )

    fig_top_customers.update_layout(
        xaxis_title="Sales",
        yaxis_title="Customer Name",
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(fig_top_customers, use_container_width=True)
    st.dataframe(top_customers, use_container_width=True)

else:
    st.info("Customer Name column is not available in this dataset.")


# ------------------------------------------------------------
# Sub-Category Performance
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Sub-Category Performance")

subcategory_performance = (
    filtered_df
    .groupby("sub_category", as_index=False)
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        average_profit_margin=("profit_margin", "mean")
    )
    .sort_values(by="total_sales", ascending=False)
)

fig_subcategory = px.bar(
    subcategory_performance,
    x="sub_category",
    y="total_sales",
    color="total_profit",
    title="Sales and Profit by Sub-Category",
    text_auto=".2s"
)

fig_subcategory.update_layout(
    xaxis_title="Sub-Category",
    yaxis_title="Sales"
)

st.plotly_chart(fig_subcategory, use_container_width=True)
st.dataframe(subcategory_performance, use_container_width=True)


# ------------------------------------------------------------
# Monthly Sales and Profit Trend
# ------------------------------------------------------------

if "year_month" in filtered_df.columns:
    st.markdown("---")
    st.subheader("Monthly Sales and Profit Trend")

    monthly_sales_profit = (
        filtered_df
        .groupby("year_month", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum")
        )
        .sort_values(by="year_month")
    )

    fig_monthly_trend = px.line(
        monthly_sales_profit,
        x="year_month",
        y=["total_sales", "total_profit"],
        title="Monthly Sales and Profit Trend",
        markers=True
    )

    fig_monthly_trend.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount"
    )

    st.plotly_chart(fig_monthly_trend, use_container_width=True)


# ------------------------------------------------------------
# Filtered Data Preview
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Filtered Data Preview")

st.dataframe(filtered_df.head(100), use_container_width=True)


# ------------------------------------------------------------
# Download Filtered Data
# ------------------------------------------------------------

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_global_superstore_data.csv",
    mime="text/csv"
)


# ------------------------------------------------------------
# Business Insights
# ------------------------------------------------------------

st.markdown("---")
st.subheader("Business Insights")

best_region = sales_by_region.iloc[0]["region"]
best_region_sales = sales_by_region.iloc[0]["sales"]

most_profitable_category = profit_by_category.iloc[0]["category"]
most_profitable_category_profit = profit_by_category.iloc[0]["profit"]

st.markdown(
    f"""
    ### Key Insights from Current Filters

    - The highest-sales region is **{best_region}**, generating **${best_region_sales:,.0f}** in sales.
    - The most profitable category is **{most_profitable_category}**, generating **${most_profitable_category_profit:,.0f}** in profit.
    - Total filtered sales are **${total_sales:,.0f}**.
    - Total filtered profit is **${total_profit:,.0f}**.
    - Average profit margin is **{average_profit_margin:.2f}%**.
    """
)

if total_profit < 0:
    st.warning(
        "The selected filters show negative total profit. The business should review discounts, shipping costs, and low-margin products."
    )

elif average_profit_margin < 5:
    st.warning(
        "The selected data has a low profit margin. The business should reduce excessive discounts and focus on higher-margin products."
    )

else:
    st.success(
        "The selected business segment is profitable under the current filters."
    )
