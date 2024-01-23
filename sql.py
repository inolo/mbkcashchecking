import sqlite3

conn = sqlite3.connect('cashchecking.db')

cur = conn.cursor()

create_customers_table = '''
CREATE TABLE CUSTOMERS 

(
  customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  customer_uuid TEXT ,
  phone_number TEXT,
  address TEXT,
  license_number TEXT,
  creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_checked_date TIMESTAMP,
  customer_photo TEXT,
  customer_license_photo TEXT,
  is_flagged BOOLEAN DEFAULT 0,
  notes TEXT DEFAULT 'NO NOTES'
  )
'''

create_order_table = '''
 CREATE TABLE ORDERS 
 (
  
  order_id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_uuid TEXT,
  customer_id INTEGER,
  customer_uuid TEXT,
  order_create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  date_check_issued TIMESTAMP,
  company TEXT,
  check_number TEXT,
  check_account_number INTEGER,
  amount INTEGER, 
  check_photo TEXT,
  employee_id INTEGER
 )

'''

create_employees_table = '''
 CREATE TABLE EMPLOYEES
 (employee_id INTEGER,
 first_name TEXT,
 last_name TEXT,
 creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 last_login TIMESTAMP,
 password TEXT,
 username TEXT
 )
'''

cur.execute(create_order_table)
cur.execute(create_customers_table)
cur.execute(create_employees_table)
conn.commit()


