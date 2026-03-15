import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime, timedelta

print("ML Libraries loaded successfully!")
#Load Data
sales = pd.read_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\sales_orders.csv')
products = pd.read_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\products.csv')

print(f"✅ Sales data loaded: {len(sales)} rows")
print(f"✅ Products data loaded: {len(products)} rows")

sales['Order_Date']=pd.to_datetime(sales['Order_Date'])

#Extract Date Features
sales['Month']=sales['Order_Date'].dt.month
sales['Year']=sales['Order_Date'].dt.year
sales['Quarter']=sales['Order_Date'].dt.quarter
sales['Day_of_Week']=sales['Order_Date'].dt.dayofweek

#Group Of Month
monthly_demand=sales.groupby(
    ['Year', 'Month', 'Quarter', 'Product_ID']
).agg(
    Total_Quantity=('Quantity','sum'),
    Total_Amount=('Total_Amount','sum'),
    Order_Count=('Order_ID','nunique'),
).reset_index()

print(f"✅ Monthly demand prepared: {len(monthly_demand)} rows")
print(monthly_demand.head())

#Features for Prediction
feautures=['Year','Month','Quarter']
target='Total_Quantity'

# Prepare X and y
X = monthly_demand[['Year', 'Month', 'Quarter']].values
y = monthly_demand['Total_Quantity'].values

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
from sklearn.linear_model import LinearRegression as LR
model = LR()
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

# Accuracy
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"📊 Mean Absolute Error: {mae:.2f}")
print(f"📊 R2 Score: {r2:.2f}")

# Add more features
monthly_demand['Product_Num'] = monthly_demand['Product_ID'].str.extract('(\d+)').astype(int)

# Features for prediction
X = monthly_demand[[
    'Year', 
    'Month', 
    'Quarter',
    'Product_Num',
    'Order_Count'
]].values

y = monthly_demand['Total_Quantity'].values

future_months=[]
for month in range(1,7):
    future_months.append({
        'Year':2026,
        'Month':month,
        'Quarter':(month-1)//3+1,


    })
    future_df=pd.DataFrame(future_months)
    future_predictions=model.predict(future_df.values)
    future_df['Predicted_Quantity']=future_predictions.astype(int)

    print(f"✅ Future demand predicted!")
    print(future_df[['Year', 'Month', 'Predicted_Quantity']])

    future_df.to_csv(
    r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\demand_forecast.csv',
    index=False)
    print(f"✅ Forecast saved to data folder!")