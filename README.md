
# Task 5: Interactive Business Dashboard in Streamlit

## Project Overview

This project is an interactive business dashboard developed using Streamlit and the Global Superstore Dataset.

The dashboard allows users to analyze sales, profit, customer performance, product category performance, and segment-wise business performance through interactive filters and visualizations.

## Task Objective

The objective of this task is to develop an interactive dashboard for analyzing:

- Total Sales
- Total Profit
- Segment-wise performance
- Region-wise performance
- Category and Sub-Category performance
- Top 5 Customers by Sales

## Dataset

The dataset used is the Global Superstore Dataset.

The dataset contains order-level retail sales data, including:

- Order ID
- Order Date
- Customer Name
- Segment
- Region
- Category
- Sub-Category
- Product Name
- Sales
- Profit
- Quantity
- Discount
- Shipping Cost

## Approach

The project was completed through the following steps:

1. Loaded the Global Superstore dataset.
2. Cleaned and standardized column names.
3. Converted date columns into datetime format.
4. Converted numerical columns such as Sales, Profit, Quantity, Discount, and Shipping Cost into numeric format.
5. Removed duplicate records.
6. Removed rows with missing critical values.
7. Created additional business metrics such as Profit Margin and Year-Month.
8. Built an interactive Streamlit dashboard.
9. Added filters for Region, Category, and Sub-Category.
10. Created KPI cards and business visualizations.
11. Added filtered data preview and download option.
12. Generated business insights based on selected filters.

## Dashboard Features

The dashboard includes:

- Region filter
- Category filter
- Sub-Category filter
- Total Sales KPI
- Total Profit KPI
- Total Orders KPI
- Average Profit Margin KPI
- Sales by Region chart
- Profit by Category chart
- Sales by Segment chart
- Top 5 Customers by Sales chart
- Sales and Profit by Sub-Category chart
- Monthly Sales and Profit Trend chart
- Filtered data preview
- Download filtered data option
- Dynamic business insights

## Visualizations

The dashboard contains the following important visuals:

### Sales by Region

This chart shows which regions generate the highest sales.

### Profit by Category

This chart identifies the most profitable product categories.

### Sales Share by Segment

This pie chart shows how sales are distributed across customer segments.

### Top 5 Customers by Sales

This chart identifies the highest-value customers based on total sales.

### Sub-Category Performance

This chart compares sales and profit across product sub-categories.

### Monthly Sales and Profit Trend

This line chart shows how sales and profit change over time.

## Results and Findings

The dashboard helps identify:

- Which regions generate the highest sales
- Which categories are most profitable
- Which customers contribute the most revenue
- Which sub-categories perform well or poorly
- Whether filtered business segments are profitable
- How sales and profit change over time

## Business Insights

The dashboard provides practical business intelligence for retail decision-making.

Key insights include:

- High-sales regions should receive stronger inventory and marketing support.
- Low-profit categories should be reviewed for discounting, pricing, and shipping costs.
- Top customers can be targeted with loyalty programs and personalized offers.
- Sub-category analysis can help identify products that should be promoted, improved, or discontinued.
- Monthly trends can support sales planning and seasonal strategy.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
````

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

## Final Conclusion

This project successfully developed an interactive Streamlit dashboard for the Global Superstore Dataset.

The dashboard transforms raw sales data into meaningful business insights through KPIs, filters, visualizations, and dynamic analysis. It can help managers monitor performance, identify profitable areas, understand customer value, and make better marketing and sales decisions.
