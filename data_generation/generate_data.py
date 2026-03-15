import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

print("✅ All libraries loaded successfully!")


categories=['Electronics','Packaging','Raw Materials', 'Spare Parts', 'Consumables']
subcategories={
    'Electronics':['Sensors','Controllers','Displays'],
    'Packaging': ['Boxes', 'Pallets', 'Wrapping'],
    'Raw Materials': ['Steel', 'Plastic', 'Aluminium'],
    'Spare Parts': ['Bearings', 'Belts', 'Filters'],
    'Consumables': ['Lubricants', 'Chemicals', 'Adhesives']
}

products=[]
for i in range (1,101):
    category=random.choice(categories)
    subcategory=random.choice(subcategories[category])
    products.append({
        'Product_ID': f'PRD{i:04d}',
        'Product_Name': f'{subcategory} {fake.word().capitalize()} {i}',
        'Category': category,
        'Subcategory': subcategory,
        'Unit_Price': round(random.uniform(10, 5000), 2),
        'Unit_Cost': round(random.uniform(5, 3000), 2),
        'Lead_Time_Days': random.randint(1, 30),
        'Reorder_Point': random.randint(10, 100),
        'Safety_Stock': random.randint(5, 50),
        'UOM': random.choice(['KG', 'PCS', 'LTR', 'MTR', 'BOX'])
    })
    df_products = pd.DataFrame(products)
    df_products.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\products.csv', index=False)
    print(f"✅ Products table created: {len(df_products)} rows")

    countries=['India','China','USA','Germany','Japan','UK','Vietnam','Brazil']
    supplier_types=['Manufacturer', 'Distributor', 'Wholesaler', 'Trader']
    suppliers=[]
    for i in range(1,31): #30 suppliers
        suppliers.append({
            'Supplier_ID':f'SUP{i:03d}',
            'Supplier_Name': fake.company(),
            'Country': random.choice(countries),
            'City': fake.city(),
            'Supplier_Type': random.choice(supplier_types),
            'Contact_Person': fake.name(),
            'Email': fake.email(),
            'Phone': fake.phone_number(),
            'Rating': round(random.uniform(1, 5), 1),
            'Payment_Terms_Days': random.choice([15, 30, 45, 60, 90]),
            'On_Time_Delivery_Rate': round(random.uniform(60, 100), 1),
            'Active': random.choice(['Yes', 'Yes', 'Yes', 'No'])
        })
        df_suppliers=pd.DataFrame(suppliers)
        df_suppliers.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\suppliers.csv', index=False)
        print(f"✅ Suppliers table created: {len(df_suppliers)} rows")

        warehouses = []
        warehouse_locations = [
            ('Chennai', 'Tamil Nadu'), ('Mumbai', 'Maharashtra'),
            ('Delhi', 'Delhi'), ('Bangalore', 'Karnataka'),
            ('Hyderabad', 'Telangana'), ('Pune', 'Maharashtra'),
            ('Kolkata', 'West Bengal'), ('Ahmedabad', 'Gujarat')
        ]
        for i,(city,state)in enumerate(warehouse_locations,1):
            warehouses.append({
                'Warehouse_ID':f'WH{i:03d}',
                'Warehouse_Name':f'{city} Warehouse',
                'City':city,
                'State':state,
                'Country':'India',
                'Capacity_Units':random.randint(5000,50000),

            })
    df_warehouses = pd.DataFrame(warehouses)
    df_warehouses.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\warehouses.csv', index=False)
    print(f"✅ Warehouses table created: {len(df_warehouses)} rows")

    # ============================================
# TABLE 4 - CUSTOMERS
# ============================================

customer_segments = ['Retail', 'Wholesale', 'Industrial', 'Government', 'E-Commerce']
indian_cities = [
    'Chennai', 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad',
    'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Surat',
    'Lucknow', 'Kanpur', 'Nagpur', 'Coimbatore', 'Kochi'
]

customers = []
for i in range(1, 201):  # 200 customers
    customers.append({
        'Customer_ID': f'CUST{i:04d}',
        'Customer_Name': fake.company(),
        'Segment': random.choice(customer_segments),
        'City': random.choice(indian_cities),
        'State': fake.state(),
        'Country': 'India',
        'Contact_Person': fake.name(),
        'Email': fake.email(),
        'Phone': fake.phone_number(),
        'Credit_Limit': round(random.uniform(10000, 500000), 2),
        'Payment_Terms_Days': random.choice([15, 30, 45, 60]),
        'Active': random.choice(['Yes', 'Yes', 'Yes', 'No'])
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\customers.csv', index=False)

#Table5-Inventory

# ============================================
# TABLE 5 - INVENTORY
# ============================================

inventory = []
for i, product in df_products.iterrows():
    for _, warehouse in df_warehouses.iterrows():
        if random.random() > 0.3:  # 70% chance product exists in warehouse
            stock = random.randint(0, 1000)
            reorder_point = product['Reorder_Point']
            inventory.append({
                'Inventory_ID': f'INV{len(inventory)+1:05d}',
                'Product_ID': product['Product_ID'],
                'Warehouse_ID': warehouse['Warehouse_ID'],
                'Stock_Quantity': stock,
                'Reorder_Point': reorder_point,
                'Safety_Stock': product['Safety_Stock'],
                'Stock_Status': 'Critical' if stock < product['Safety_Stock']
                                else 'Low' if stock < reorder_point
                                else 'Normal',
                'Last_Updated': fake.date_between(
                    start_date='-30d', end_date='today'),
                'Unit_Cost': product['Unit_Cost'],
                'Total_Value': round(stock * product['Unit_Cost'], 2)
            })

df_inventory = pd.DataFrame(inventory)
df_inventory.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\inventory.csv', index=False)
print(f"✅ Inventory table created: {len(df_inventory)} rows")

# ============================================
# TABLE 6 - PURCHASE ORDERS
# ============================================

po_statuses = ['Delivered', 'Delivered', 'Delivered', 'In Transit', 'Pending', 'Cancelled']

purchase_orders = []
for i in range(1, 501):  # 500 purchase orders
    product = df_products.sample(1).iloc[0]
    supplier = df_suppliers.sample(1).iloc[0]
    warehouse = df_warehouses.sample(1).iloc[0]
    order_date = fake.date_between(start_date='-365d', end_date='today')
    lead_time = product['Lead_Time_Days']
    expected_delivery = expected_delivery = order_date + timedelta(days=int(lead_time))
    status = random.choice(po_statuses)
    actual_delivery = None
    if status == 'Delivered':
        delay = random.randint(-3, 10)
        actual_delivery = expected_delivery + timedelta(days=delay)

    quantity = random.randint(10, 500)
    unit_cost = product['Unit_Cost']

    purchase_orders.append({
        'PO_ID': f'PO{i:05d}',
        'Product_ID': product['Product_ID'],
        'Supplier_ID': supplier['Supplier_ID'],
        'Warehouse_ID': warehouse['Warehouse_ID'],
        'Order_Date': order_date,
        'Expected_Delivery': expected_delivery,
        'Actual_Delivery': actual_delivery,
        'Quantity_Ordered': quantity,
        'Quantity_Received': quantity if status == 'Delivered' else 0,
        'Unit_Cost': round(unit_cost, 2),
        'Total_Cost': round(quantity * unit_cost, 2),
        'Status': status,
        'On_Time': 'Yes' if status == 'Delivered' and actual_delivery <= expected_delivery else 'No'
    })

df_purchase_orders = pd.DataFrame(purchase_orders)
df_purchase_orders.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\purchase_orders.csv', index=False)
print(f"✅ Purchase Orders table created: {len(df_purchase_orders)} rows")

# ============================================
# TABLE 7 - SALES ORDERS
# ============================================

order_statuses = ['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Processing', 'Cancelled']

sales_orders = []
for i in range(1, 1001):  # 1000 sales orders
    product = df_products.sample(1).iloc[0]
    customer = df_customers.sample(1).iloc[0]
    warehouse = df_warehouses.sample(1).iloc[0]
    order_date = fake.date_between(start_date='-365d', end_date='today')
    expected_delivery = order_date + timedelta(days=random.randint(1, 14))
    status = random.choice(order_statuses)
    actual_delivery = None
    if status == 'Delivered':
        delay = random.randint(-2, 7)
        actual_delivery = expected_delivery + timedelta(days=delay)

    quantity = random.randint(1, 100)
    unit_price = product['Unit_Price']
    discount = round(random.uniform(0, 0.2), 2)

    sales_orders.append({
        'Order_ID': f'SO{i:05d}',
        'Product_ID': product['Product_ID'],
        'Customer_ID': customer['Customer_ID'],
        'Warehouse_ID': warehouse['Warehouse_ID'],
        'Order_Date': order_date,
        'Expected_Delivery': expected_delivery,
        'Actual_Delivery': actual_delivery,
        'Quantity': quantity,
        'Unit_Price': round(unit_price, 2),
        'Discount_Pct': discount,
        'Total_Amount': round(quantity * unit_price * (1 - discount), 2),
        'Status': status,
        'On_Time': 'Yes' if status == 'Delivered' and actual_delivery <= expected_delivery else 'No',
        'Region': customer['City']
    })

df_sales_orders = pd.DataFrame(sales_orders)
df_sales_orders.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\sales_orders.csv', index=False)
print(f"✅ Sales Orders table created: {len(df_sales_orders)} rows")

# TABLE 8 - SHIPMENTS


carriers = ['FedEx', 'DHL', 'Blue Dart', 'DTDC', 'Delhivery', 'Ecom Express', 'XpressBees']
ship_modes = ['Air', 'Road', 'Rail', 'Sea']

shipments = []
delivered_orders = df_sales_orders[df_sales_orders['Status'].isin(['Delivered', 'Shipped'])]

for i, (_, order) in enumerate(delivered_orders.iterrows(), 1):
    carrier = random.choice(carriers)
    ship_mode = random.choice(ship_modes)
    ship_date = order['Order_Date'] + timedelta(days=random.randint(1, 3))
    expected = order['Expected_Delivery']
    actual = order['Actual_Delivery'] if order['Status'] == 'Delivered' else None

    shipments.append({
        'Shipment_ID': f'SHP{i:05d}',
        'Order_ID': order['Order_ID'],
        'Carrier': carrier,
        'Ship_Mode': ship_mode,
        'Ship_Date': ship_date,
        'Expected_Delivery': expected,
        'Actual_Delivery': actual,
        'Shipping_Cost': round(random.uniform(50, 2000), 2),
        'Weight_KG': round(random.uniform(0.5, 500), 2),
        'Status': order['Status'],
        'On_Time': order['On_Time'],
        'Delay_Days': max(0, (actual - expected).days) if actual else 0
    })

df_shipments = pd.DataFrame(shipments)
df_shipments.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\shipments.csv', index=False)
print(f"✅ Shipments table created: {len(df_shipments)} rows")

# TABLE 9 - PRODUCTION ORDERS
production_lines = ['Line A', 'Line B', 'Line C', 'Line D']
production_statuses = ['Completed', 'Completed', 'Completed', 'In Progress', 'Planned', 'On Hold']

production_orders = []
for i in range(1, 401):  # 400 production orders
    product = df_products.sample(1).iloc[0]
    warehouse = df_warehouses.sample(1).iloc[0]
    start_date = fake.date_between(start_date='-365d', end_date='today')
    planned_days = random.randint(1, 14)
    planned_end = start_date + timedelta(days=planned_days)
    status = random.choice(production_statuses)
    actual_end = None
    if status == 'Completed':
        delay = random.randint(-2, 5)
        actual_end = planned_end + timedelta(days=delay)

    planned_qty = random.randint(50, 1000)
    actual_qty = int(planned_qty * random.uniform(0.85, 1.0)) if status == 'Completed' else 0

    production_orders.append({
        'Production_ID': f'PRO{i:05d}',
        'Product_ID': product['Product_ID'],
        'Warehouse_ID': warehouse['Warehouse_ID'],
        'Production_Line': random.choice(production_lines),
        'Start_Date': start_date,
        'Planned_End_Date': planned_end,
        'Actual_End_Date': actual_end,
        'Planned_Quantity': planned_qty,
        'Actual_Quantity': actual_qty,
        'Status': status,
        'Efficiency_Pct': round((actual_qty / planned_qty) * 100, 1) if planned_qty > 0 and status == 'Completed' else 0,
        'On_Time': 'Yes' if status == 'Completed' and actual_end <= planned_end else 'No'
    })

df_production = pd.DataFrame(production_orders)
df_production.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\production_orders.csv', index=False)
print(f"✅ Production Orders table created: {len(df_production)} rows") 

#Date Table

date_range = pd.date_range(start='2024-01-01', end='2025-12-31', freq='D')

date_table = []
for date in date_range:
    date_table.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Day': date.day,
        'Month': date.month,
        'Month_Name': date.strftime('%B'),
        'Month_Short': date.strftime('%b'),
        'Quarter': f'Q{date.quarter}',
        'Quarter_No': date.quarter,
        'Year': date.year,
        'Year_Month': date.strftime('%Y-%m'),
        'Week_No': date.isocalendar()[1],
        'Day_Name': date.strftime('%A'),
        'Day_of_Week': date.dayofweek + 1,
        'Is_Weekend': 'Yes' if date.dayofweek >= 5 else 'No',
        'Financial_Year': f'FY{date.year}' if date.month >= 4 else f'FY{date.year - 1}'
    })

df_dates = pd.DataFrame(date_table)
df_dates.to_csv(r'C:\Users\vinothkumar\SCM_Analytics_Platform\data\date_table.csv', index=False)
print(f"✅ Date table created: {len(df_dates)} rows")
print("")
print("🎉 ALL TABLES GENERATED SUCCESSFULLY!")
print(f"   📦 Products      : {len(df_products)} rows")
print(f"   🏭 Suppliers     : {len(df_suppliers)} rows")
print(f"   🏢 Warehouses    : {len(df_warehouses)} rows")
print(f"   👥 Customers     : {len(df_customers)} rows")
print(f"   📊 Inventory     : {len(df_inventory)} rows")
print(f"   🛒 Purchase Orders: {len(df_purchase_orders)} rows")
print(f"   💰 Sales Orders  : {len(df_sales_orders)} rows")
print(f"   🚚 Shipments     : {len(df_shipments)} rows")
print(f"   🏗️  Production    : {len(df_production)} rows")
print(f"   📅 Date Table    : {len(df_dates)} rows")
