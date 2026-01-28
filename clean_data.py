# Project: Clean a messy customer transactions dataset
import pandas as pd

# 1 Load all datasets

customers = pd.read_csv(r'C:\datanomics\python\project\data_cleaning\file\customer_data.csv')
products = pd.read_csv(r'C:\datanomics\python\project\data_cleaning\file\product_data.csv')
sale = pd.read_csv(r'C:\datanomics\python\project\data_cleaning\file\sales_data.csv')
sales = sale.copy()
# 2 Fix column names
for df in [customers, products, sales]:
    df.columns = df.columns.str.strip().str.lower()

# 3 Parse date formats in sales
sales['date'] = pd.to_datetime(sales['date'], errors='coerce')

# 4 Remove invalid values

#  Remove transactions without ID or customer
sales.dropna(subset=['transaction_id','customer_id'], inplace=True)

#  Remove duplicates
sales.drop_duplicates(inplace=True)


# Fill missing values in sales

# 1. Fill text/object columns with 'unknown'
text_cols = sales.select_dtypes(include='object').columns
sales[text_cols] = sales[text_cols].fillna('unknown')

# 2. Fill numeric columns with 0
num_cols = sales.select_dtypes(include=['int64', 'float64']).columns
sales[num_cols] = sales[num_cols].fillna(0)

print(sales.isna().sum())
print(sales.info())
# 5 Join datasets
df = sales.merge(products, on='product_id', how='left') \
          .merge(customers, on='customer_id', how='left') \

# 6 Calculate revenue
# Revenue = quantity * list_price * (1 - discount)
df['revenue'] = df['quantity'] * df['list_price'] * (1 - df['discount'])

# 7 Aggregate revenue by month & customer
df['month'] = df['date'].dt.month # extract month

monthly_revenue = df.groupby(['customer_id','month'])['revenue'] \
                    .sum() \
                    .reset_index()


print(monthly_revenue.head())