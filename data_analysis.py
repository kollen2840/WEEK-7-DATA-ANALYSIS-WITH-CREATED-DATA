import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Create sample sales data with Kenyan market context
def create_kenyan_sales_data(num_records=1000):
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(num_records)]
    
    # Product categories with realistic Kenyan prices (in KES)
    products_and_prices = {
        # Electronics
        'Smartphone': (15000, 120000),
        'Laptop': (35000, 180000),
        'TV': (15000, 150000),
        'Radio': (2000, 8000),
        
        # Home Appliances
        'Refrigerator': (25000, 120000),
        'Microwave': (8000, 35000),
        'Water Dispenser': (5000, 25000),
        
        # Household Items
        'Gas Cooker': (3000, 45000),
        'Electric Kettle': (1500, 5000),
        'Iron Box': (1000, 4500),
        
        # Groceries and Daily Items
        'Cooking Oil (5L)': (800, 1500),
        'Maize Flour (2kg)': (150, 250),
        'Rice (2kg)': (200, 400),
        'Sugar (2kg)': (200, 300),
        
        # Personal Care
        'Body Lotion': (200, 1000),
        'Shower Gel': (150, 800),
        'Toothpaste': (100, 300)
    }
    
    regions = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Nyeri']
    store_types = ['Supermarket', 'Wholesale Shop', 'Mini Market', 'Electronics Store']
    payment_methods = ['M-Pesa', 'Cash', 'Credit Card', 'Bank Transfer']
    
    data = {
        'Date': dates,
        'Product': np.random.choice(list(products_and_prices.keys()), num_records),
        'Region': np.random.choice(regions, num_records),
        'Store_Type': np.random.choice(store_types, num_records),
        'Payment_Method': np.random.choice(payment_methods, num_records),
        'Quantity': np.random.randint(1, 20, num_records)
    }
    
    # Calculate unit prices based on product ranges
    unit_prices = []
    for product in data['Product']:
        min_price, max_price = products_and_prices[product]
        unit_prices.append(round(np.random.uniform(min_price, max_price)))
    
    data['Unit_Price'] = unit_prices
    data['Total_Sales'] = data['Quantity'] * data['Unit_Price']
    
    return pd.DataFrame(data)

# Create and save the dataset
sales_df = create_kenyan_sales_data()
sales_df.to_csv('kenya_sales_data.csv', index=False)

def analyze_kenyan_sales_data(df):
    # 1. Monthly Sales Trend
    monthly_sales = df.groupby(df['Date'].dt.strftime('%Y-%m'))['Total_Sales'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(monthly_sales)), monthly_sales['Total_Sales'] / 1000, marker='o')
    plt.title('Monthly Sales Trend (Thousands KES)')
    plt.xlabel('Month')
    plt.ylabel('Total Sales (Thousands KES)')
    plt.xticks(range(len(monthly_sales)), monthly_sales['Date'], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('kenya_monthly_sales_trend.png')
    plt.close()
    
    # 2. Product Category Performance
    product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(15, 8))
    plt.bar(range(len(product_sales)), product_sales.values)
    plt.title('Total Sales by Product')
    plt.xlabel('Product')
    plt.ylabel('Total Sales (KES)')
    plt.xticks(range(len(product_sales)), product_sales.index, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('kenya_product_sales.png')
    plt.close()
    
    # 3. Regional Performance
    regional_sales = df.groupby('Region')['Total_Sales'].sum()
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(regional_sales)), regional_sales.values)
    plt.title('Sales by Region')
    plt.xlabel('Region')
    plt.ylabel('Total Sales (KES)')
    plt.xticks(range(len(regional_sales)), regional_sales.index, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('kenya_regional_sales.png')
    plt.close()
    
    # 4. Payment Method Analysis
    plt.figure(figsize=(10, 10))
    payment_sales = df.groupby('Payment_Method')['Total_Sales'].sum()
    plt.pie(payment_sales, labels=payment_sales.index, autopct='%1.1f%%')
    plt.title('Sales Distribution by Payment Method')
    plt.tight_layout()
    plt.savefig('kenya_payment_methods.png')
    plt.close()
    
    # 5. Store Type Performance
    store_sales = df.groupby('Store_Type')['Total_Sales'].sum()
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(store_sales)), store_sales.values)
    plt.title('Sales by Store Type')
    plt.xlabel('Store Type')
    plt.ylabel('Total Sales (KES)')
    plt.xticks(range(len(store_sales)), store_sales.index, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('kenya_store_type_sales.png')
    plt.close()
    
    # Generate summary statistics
    summary_stats = {
        'Total Revenue (KES)': df['Total_Sales'].sum(),
        'Average Transaction Value (KES)': df['Total_Sales'].mean(),
        'Total Units Sold': df['Quantity'].sum(),
        'Best Selling Product (by value)': df.groupby('Product')['Total_Sales'].sum().idxmax(),
        'Best Selling Product (by volume)': df.groupby('Product')['Quantity'].sum().idxmax(),
        'Top Region': df.groupby('Region')['Total_Sales'].sum().idxmax(),
        'Most Popular Payment Method': df.groupby('Payment_Method')['Total_Sales'].sum().idxmax(),
        'Best Performing Store Type': df.groupby('Store_Type')['Total_Sales'].sum().idxmax()
    }
    
    # Additional analysis for seasonal trends
    df['Month'] = df['Date'].dt.month
    monthly_avg_sales = df.groupby('Month')['Total_Sales'].mean()
    summary_stats['Peak Sales Month'] = monthly_avg_sales.idxmax()
    
    return summary_stats

# Run the analysis
summary = analyze_kenyan_sales_data(sales_df)

# Print summary statistics
print("\nKenyan Market Sales Analysis Summary:")
print("------------------------------------")
for key, value in summary.items():
    if isinstance(value, float):
        print(f"{key}: {value:,.2f}")
    else:
        print(f"{key}: {value}")

def get_product_insights(df):
    print("\nProduct Insights:")
    print("----------------")
    product_margins = df.groupby('Product').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum'
    })
    product_margins['Average_Price'] = product_margins['Total_Sales'] / product_margins['Quantity']
    print("\nTop 5 Products by Average Price:")
    print(product_margins.sort_values('Average_Price', ascending=False).head().round(2))

def get_regional_insights(df):
    print("\nRegional Insights:")
    print("-----------------")
    regional_analysis = df.groupby('Region').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum'
    }).round(2)
    print("\nRegional Performance:")
    print(regional_analysis.sort_values('Total_Sales', ascending=False))

# Run additional analyses
get_product_insights(sales_df)
get_regional_insights(sales_df)
