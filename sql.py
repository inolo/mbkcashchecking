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
  notes TEXT DEFAULT 'NO NOTES',
  employee_id INTEGER,
  store TEXT,
  old_id INTEGER
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
  employee_id INTEGER,
  amount_issued INTEGER,
  company_id INTEGER,
  store TEXT
 )

'''

create_employees_table = '''
 CREATE TABLE employees
 (employee_id  INTEGER PRIMARY KEY AUTOINCREMENT,
 first_name TEXT,
 last_name TEXT,
 creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 last_login TIMESTAMP,
 password TEXT,
 username TEXT,
 permission TEXT,
 is_active BOOLEAN
 )
'''

create_companies_table = '''
CREATE TABLE COMPANIES 
    (company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    phone_number TEXT,
    employee_id INTEGER,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

'''

cur.execute(create_order_table)
cur.execute(create_customers_table)
cur.execute(create_employees_table)
cur.execute(create_companies_table)
cur.execute(
    """insert into employees ( first_name, last_name, password, username, permission) values ( 'Kevin', 'Nguyen', 'Ilovesushi1!', 'kevin93nguyen', 'admin')""")
cur.execute(
    """insert into employees ( first_name, last_name, password, username, permission) values ( 'ivy', 'wong', 'Ilovesushi1!', 'ivywong93', 'admin')""")
cur.execute(
    """insert into employees ( first_name, last_name, password, username, permission) values ( 'hazel', 'nguyen', 'Ilovesushi1!', 'hazel22', 'manager')""")
conn.commit()

# insert into employees ( first_name, last_name, password, username, permission) values ( 'Kevin', 'Nguyen', 'Ilovesushi1!', 'kevin93nguyen', 'admin')