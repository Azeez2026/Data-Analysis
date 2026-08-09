import pandas as pd
from sqlalchemy import create_engine
DATABASE_URL = 'postgresql+psycopg2://neondb_owner:npg_nf0Bpoz8SKtF@ep-solitary-recipe-ah9qonat-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require'
engine = create_engine(DATABASE_URL)
df_customers = pd.read_sql_query('SELECT * FROM oms_core.customers;', engine)
df_customers = df_customers[df_customers['customerid'].notnull()]
email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
df_customers = df_customers[df_customers['email'].astype(str).str.match(email_regex, na=False)]
df_customers.to_csv('customers_clean.csv', index=False)
df_orders = pd.read_sql_query('SELECT * FROM oms_core.orders;', engine)
df_orders = df_orders[df_orders['orderdate'].notnull()]
df_orders.to_csv('orders_clean.csv', index=False)
df_orderitems = pd.read_sql_query('SELECT * FROM oms_core.orderitems;', engine)
df_orderitems = df_orderitems[df_orderitems['quantity'] > 0]
df_orderitems.to_csv('orderitems_clean.csv', index=False)
df_products = pd.read_sql_query('SELECT * FROM oms_core.products;', engine)
df_products = df_products[df_products['retailprice'] >= df_products['supplierprice']]
df_products.to_csv('products_clean.csv', index=False)
df_employees = pd.read_sql_query('SELECT * FROM oms_core.employees;', engine)
df_employees['hiredate'] = pd.to_datetime(df_employees['hiredate'])
df_employees = df_employees[df_employees['hiredate'] <= pd.Timestamp.now()]
df_employees.to_csv('employees_clean.csv', index=False)
other_tables = ['dates', 'stores', 'suppliers']
for table in other_tables:
    df = pd.read_sql_query(f'SELECT * FROM oms_core.{table};', engine)
    df.to_csv(f'{table}_clean.csv', index=False)