import sqlite3

def get_db_companies(cursor, filter):
    sql = '''
    SELECT name FROM companies WHERE name LIKE ?
    '''
    cursor.execute(sql, ('%' + filter + '%',))
    results = cursor.fetchall()
    return results

def get_db_companies_detail(cursor, filter):
    sql = '''
    SELECT address, phone_number FROM companies WHERE name = ?
    '''
    cursor.execute(sql, (filter,))
    results = cursor.fetchone()
    return results

def get_report_data(cursor, date_to, date_from):
    sql = '''
    SELECT order_id, customer_id, order_create_date, amount, employee_id, amount_issued 
    FROM orders 
    WHERE order_create_date > ? AND order_create_date < ?
    '''
    cursor.execute(sql, (date_from, date_to))
    results = cursor.fetchall()
    return results

def get_user(cursor, password, username):
    sql = '''
    SELECT employee_id, first_name, last_name, permission 
    FROM employees 
    WHERE password = ? AND username = ?
    '''
    cursor.execute(sql, (password, username))
    results = cursor.fetchone()
    return results

def get_db_customers(cursor):
    sql = '''
    SELECT customer_id, first_name, last_name, phone_number, is_flagged FROM customers
    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def get_company_list(cursor, date_from=None, date_to=None, text=None):
    sql = '''
    SELECT company_id, name, address, phone_number, creation_date
    FROM companies
    '''

    if text:
        sql += 'WHERE company_id = ? or name like ? '''
        params = (text, '%' + text + '%',)
    elif date_from and date_to:
        sql += 'WHERE creation_date <= ? AND creation_date >= ? '
        params = (date_from, date_to)
    elif date_from:
        sql += 'WHERE creation_date <= ? '
        params = (date_from,)
    elif date_to:
        sql += 'WHERE creation_date >= ? '
        params = (date_to,)
    else:
        params = ()

    sql += ' ORDER BY name asc'
    cursor.execute(sql, params)
    results = cursor.fetchall()
    return results

def get_order_list(cursor, date_from=None, date_to=None, text=None):
    sql = '''
    SELECT order_id, customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued 
    FROM orders
    '''

    if text:
        sql += 'WHERE order_id = ? OR customer_id = ? '
        params = (text, text)
    elif date_from and date_to:
        sql += 'WHERE order_create_date <= ? AND order_create_date >= ? '
        params = (date_from, date_to)
    elif date_from:
        sql += 'WHERE order_create_date <= ? '
        params = (date_from,)
    elif date_to:
        sql += 'WHERE order_create_date >= ? '
        params = (date_to,)
    else:
        params = ()

    sql += 'ORDER BY order_create_date DESC'
    cursor.execute(sql, params)
    results = cursor.fetchall()
    return results

def get_customer_list(cursor, date_from=None, date_to=None, text=None):
    sql = '''
    SELECT customer_id, first_name, last_name, phone_number, address, license_number, creation_date, last_checked_date 
    FROM customers
    '''
    conditions = []
    params = []

    if text:
        conditions.append("(first_name LIKE ? OR last_name LIKE ? OR license_number = ? OR phone_number = ? OR customer_id = ?)")
        params += ['%' + text + '%', '%' + text + '%', text, text, text]
    if date_from and date_to:
        conditions.append("creation_date <= ? AND creation_date >= ?")
        params += [date_from, date_to]

    if conditions:
        sql += 'WHERE ' + ' AND '.join(conditions)

    cursor.execute(sql, params)
    results = cursor.fetchall()
    return results


def get_company_detail(cursor, company_id):
    company_sql = '''
    SELECT company_id, name, address, phone_number, creation_date
    FROM companies
    WHERE company_id = ?
    '''
    cursor.execute(company_sql, (company_id,))
    company_result = cursor.fetchone()

    order_sql = '''
    SELECT  
    order_id ,
  customer_id ,
  order_create_date,
  date_check_issued ,
  company ,
  check_number ,
  check_account_number ,
  amount,
  employee_id ,
  amount_issued ,
  company_id  FROM orders WHERE company_id = ?
    '''
    cursor.execute(order_sql, (company_id,))
    order_result = cursor.fetchall()

    customer_sql = '''
    SELECT distinct  
      c.customer_id ,
      c.first_name ,
      c.last_name ,
      c.phone_number ,
      c.address ,
      c.license_number ,
      c.creation_date,
      c.last_checked_date ,
      c.is_flagged,
      c.notes,
      c.employee_id
     FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    WHERE o.company_id = ?
    '''
    cursor.execute(customer_sql, (company_id,))
    customer_result = cursor.fetchall()

    return company_result, order_result, customer_result
# def get_company_detail(cursor, company_id):
#     sql = f'''
#     SELECT company_id, name, address, phone_number, creation_date
#     FROM companies
#     where company_id = '{company_id}'
#     '''
#     cursor.execute(sql)
#     company_result = cursor.fetchone()
#
#     sql = f'''
#     select * from orders where company_id = '{company_id}'
#     '''
#     cursor.execute(sql)
#     order_result = cursor.fetchall()
#
#
#     sql = f'''
#     select c.* from
#     customers c
#     orders o
#     where o.customer_id = c.customer_id
#     and o.company_id = '{company_id}'
#     '''
#     cursor.execute(sql)
#     customer_result = cursor.fetchall()
#
#     return company_result, order_result, customer_result

def get_order_detail(cursor, order_id):
    sql = '''
    SELECT order_id, customer_id, order_create_date, date_check_issued, check_number, amount, order_uuid, amount_issued 
    FROM orders 
    WHERE order_id = ?
    '''
    cursor.execute(sql, (order_id,))
    results = cursor.fetchall()
    return results

def get_customer_detail(cursor, customer_id):
    sql = '''
    SELECT customer_id, first_name, last_name, phone_number, address, license_number, creation_date, last_checked_date, customer_uuid, is_flagged, notes 
    FROM customers 
    WHERE customer_id = ?
    '''
    cursor.execute(sql, (customer_id,))
    results = cursor.fetchall()
    return results

def get_order_list_by_customer(cursor, customer_id):
    sql = '''
    SELECT order_id, customer_id, order_create_date, date_check_issued, check_number, amount, order_uuid, amount_issued 
    FROM orders 
    WHERE customer_id = ?
    '''
    cursor.execute(sql, (customer_id,))
    results = cursor.fetchall()
    return results


# import sqlite3
#
#
# def get_db_companies(cursor, filter):
#     sql = f'''
#     select name from companies where name like '%{filter}%'
#     '''
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return results
#
# def get_db_companies_detail(cursor, filter):
#     sql = f'''
#     select address,phone_number from companies where name = '{filter}'
#     '''
#     cursor.execute(sql)
#     results = cursor.fetchone()
#     return results
#
# def get_report_data(cursor, date_to, date_from):
#     sql = f'''
#     select order_id, customer_id, order_create_date,amount, employee_id, amount_issued from orders where order_create_date > '{date_from}' and  order_create_date < '{date_to}'
#
#     '''
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return results
#
# def get_user(cursor, password, username):
#     sql = f'''
#     select employee_id, first_name, last_name, permission from employees where password = '{password}' and username = '{username}'
#     '''
#     cursor.execute(sql)
#     results = cursor.fetchone()
#     return results
#
# def get_db_customers(cursor):
#     sql = '''
#     select customer_id,first_name, last_name, phone_number, is_flagged from customers
#     '''
#     cursor.execute(sql)
#     results = cursor.fetchall()
#
#     return results
#
#
# def get_order_list(cursor, date_from=None, date_to=None, text=None):
#     if text:
#         sql = f'''
#         select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
#         where order_id = {text} or customer_id = {text}
#         order by order_create_date desc
#         '''
#     elif date_from and date_to:
#         sql = f'''
#         select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
#         where order_create_date <= '{date_from}'
#         and order_create_date >= '{date_to}'
#         order by order_create_date desc
#         '''
#     elif date_from:
#         sql = f'''
#         select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
#         where order_create_date <= '{date_from}'
#         order by order_create_date desc
#         '''
#     elif date_to:
#         sql = f'''
#         select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
#         where order_create_date >= '{date_to}'
#         order by order_create_date desc'''
#     else:
#         sql = '''
#         select
#         order_id, customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued
#         from orders
#         order by order_create_date desc'''
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#
#     return results
#
#
# def get_customer_list(cursor, date_from=None, date_to=None, text=None):
#     if date_from and date_to and text:
#         sql = f'''
#         select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#         last_checked_date from customers
#         where first_name like '%{text}%' or last_name like '%{text}%' or license_number = '{text}'
#         or phone_number = '{text}' or customer_id = '{text}'
#         and creation_date >= '{date_to}' or last_checked_date <= '{date_from}'
#         and last_checked_date >= '{date_to}'
#         '''
#
#     elif text:
#         sql = f'''
#         select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#         last_checked_date from customers
#         where first_name like '%{text}%' or last_name like '%{text}%' or license_number = '{text}'
#         or phone_number = '{text}' or customer_id = '{text}'
#         '''
#
#     elif date_from and date_to:
#         sql = f'''
#         select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#         last_checked_date from customers
#         where creation_date <= '{date_from}'
#         and creation_date >= '{date_to}' or last_checked_date <= '{date_from}'
#         and last_checked_date >= '{date_to}'
#         '''
#     elif date_from:
#         sql = f'''
#         select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#         last_checked_date from customers
#         where creation_date <= '{date_from}' or last_checked_date <= '{date_from}'
#         '''
#     elif date_to:
#         sql = f'''
#         select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#         last_checked_date from customers
#         where creation_date >= '{date_to}' or last_checked_date >= '{date_to}' '''
#     else:
#         sql = '''
#        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
#        last_checked_date from customers '''
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#
#     return results
#
# def get_order_detail(cursor, order_id):
#     sql = f'''
#
#     select
#         order_id,
#         customer_id,
#         order_create_date,
#         date_check_issued,
#         check_number,
#         amount,
#         order_uuid,
#         amount_issued
#     from
#     orders
#     where order_id = {order_id}
#     '''
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return results
#
# def get_customer_detail(cursor, customer_id):
#     sql = f'''
#
#     select
#         customer_id,
#         first_name,
#         last_name,
#         phone_number,
#         address,
#         license_number,
#         creation_date,
#         last_checked_date,
#         customer_uuid,
#         is_flagged,
#         notes
#     from
#     customers
#     where customer_id = {customer_id}
#     '''
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return results
#
#
# def get_order_list_by_customer(cursor, customer_id):
#     sql = f'''
#
#     select
#         order_id,
#         customer_id,
#         order_create_date,
#         date_check_issued,
#         check_number,
#         amount,
#         order_uuid,
#         amount_issued
#
#     from
#     orders
#     where customer_id = {customer_id}
#     '''
#
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return results