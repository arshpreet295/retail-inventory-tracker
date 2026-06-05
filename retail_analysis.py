import pandas as pd
import matplotlib.pyplot as plt
import os

# Load Data
df = pd.read_csv(r'C:\Users\arshpreet\OneDrive\Desktop\retail-inventory-tracker\data\retail_sales_dataset.csv')


# Basic Cleaning
print("Shape:", df.shape)
print(df.head())
print(df.isnull().sum())

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)


df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(df.columns)  

# ---- ANALYSIS ----

# 1. Total Sales by Product Category
category_sales = df.groupby('product_category')['total_amount'].sum().reset_index()
category_sales.columns = ['Category', 'Total Sales']
print(category_sales)

# 2. Monthly Sales Trend
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
monthly_sales = df.groupby('month')['total_amount'].sum().reset_index()
monthly_sales.columns = ['Month', 'Total Sales']
print(monthly_sales)

# 3. Top 10 Customers by Revenue
top_customers = df.groupby('customer_id')['total_amount'].sum().nlargest(10).reset_index()
top_customers.columns = ['Customer ID', 'Total Revenue']
print(top_customers)

# 4. Gender-wise Sales
gender_sales = df.groupby('gender')['total_amount'].sum().reset_index()

# ---- CHARTS ----

os.makedirs('charts', exist_ok=True)

# Chart 1 - Category Sales
plt.figure(figsize=(8,5))
plt.bar(category_sales['Category'], category_sales['Total Sales'], color='steelblue')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.savefig('charts/category_sales.png')
plt.close()

# Chart 2 - Monthly Trend
plt.figure(figsize=(10,5))
plt.plot(monthly_sales['Month'].astype(str), monthly_sales['Total Sales'], marker='o', color='green')
plt.title('Monthly Sales Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('charts/monthly_trend.png')
plt.close()

# ---- EXPORT TO EXCEL ----

with pd.ExcelWriter('retail_cleaned.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Cleaned Data', index=False)
    category_sales.to_excel(writer, sheet_name='Category Sales', index=False)
    monthly_sales.to_excel(writer, sheet_name='Monthly Trend', index=False)
    top_customers.to_excel(writer, sheet_name='Top Customers', index=False)
    gender_sales.to_excel(writer, sheet_name='Gender Sales', index=False)

print("Excel file exported successfully!")
print("Charts saved in /charts folder!")
