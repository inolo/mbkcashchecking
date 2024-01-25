import sqlite3


def get_report_data(cursor, date_to, date_from):
    sql = f'''
    select order_id, customer_id, order_create_date,amount, employee_id, amount_issued from orders where order_create_date > '{date_from}' and  order_create_date < '{date_to}'

    '''
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def get_user(cursor, password, username):
    sql = f'''
    select employee_id, first_name, last_name, permission from employees where password = '{password}' and username = '{username}' 
    '''
    cursor.execute(sql)
    results = cursor.fetchone()
    return results

def get_db_customers(cursor):
    sql = '''
    select customer_id,first_name, last_name, phone_number, is_flagged from customers
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    return results


def get_order_list(cursor, date_from=None, date_to=None, text=None):
    if text:
        sql = f'''
        select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
        where order_id = {text} or customer_id = {text}
        order by order_create_date desc
        '''
    elif date_from and date_to:
        sql = f'''
        select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
        where order_create_date <= '{date_from}'
        and order_create_date >= '{date_to}'
        order by order_create_date desc
        '''
    elif date_from:
        sql = f'''
        select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
        where order_create_date <= '{date_from}'
        order by order_create_date desc
        '''
    elif date_to:
        sql = f'''
        select order_id,customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued from orders
        where order_create_date >= '{date_to}'
        order by order_create_date desc'''
    else:
        sql = '''
        select
        order_id, customer_id, order_create_date, date_check_issued, check_number, amount, amount_issued
        from orders 
        order by order_create_date desc'''

    cursor.execute(sql)
    results = cursor.fetchall()

    return results


def get_customer_list(cursor, date_from=None, date_to=None, text=None):
    if date_from and date_to and text:
        sql = f'''
        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
        last_checked_date from customers
        where first_name like '%{text}%' or last_name like '%{text}%' or license_number = '{text}'
        or phone_number = '{text}' or customer_id = '{text}' 
        and creation_date >= '{date_to}' or last_checked_date <= '{date_from}'
        and last_checked_date >= '{date_to}' 
        '''

    elif text:
        sql = f'''
        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
        last_checked_date from customers
        where first_name like '%{text}%' or last_name like '%{text}%' or license_number = '{text}'
        or phone_number = '{text}' or customer_id = '{text}' 
        '''

    elif date_from and date_to:
        sql = f'''
        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
        last_checked_date from customers
        where creation_date <= '{date_from}'
        and creation_date >= '{date_to}' or last_checked_date <= '{date_from}'
        and last_checked_date >= '{date_to}' 
        '''
    elif date_from:
        sql = f'''
        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
        last_checked_date from customers
        where creation_date <= '{date_from}' or last_checked_date <= '{date_from}'
        '''
    elif date_to:
        sql = f'''
        select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
        last_checked_date from customers
        where creation_date >= '{date_to}' or last_checked_date >= '{date_to}' '''
    else:
        sql = '''
       select customer_id,first_name, last_name, phone_number, address, license_number, creation_date,
       last_checked_date from customers '''

    cursor.execute(sql)
    results = cursor.fetchall()

    return results

def get_order_detail(cursor, order_id):
    sql = f'''
    
    select         
        order_id,
        customer_id,
        order_create_date,
        date_check_issued,
        check_number,
        amount,
        order_uuid,
        amount_issued
    from 
    orders
    where order_id = {order_id}
    '''

    cursor.execute(sql)
    results = cursor.fetchall()
    return results

def get_customer_detail(cursor, customer_id):
    sql = f'''

    select         
        customer_id,
        first_name,
        last_name,
        phone_number,
        address,
        license_number,
        creation_date,
        last_checked_date,
        customer_uuid,
        is_flagged,
        notes
    from 
    customers
    where customer_id = {customer_id}
    '''

    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def get_order_list_by_customer(cursor, customer_id):
    sql = f'''

    select         
        order_id,
        customer_id,
        order_create_date,
        date_check_issued,
        check_number,
        amount,
        order_uuid,
        amount_issued
        
    from 
    orders
    where customer_id = {customer_id}
    '''

    cursor.execute(sql)
    results = cursor.fetchall()
    return results