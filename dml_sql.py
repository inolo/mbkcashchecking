def add_user(cursor, data):
    first_name = data['firstName']
    last_name = data['lastName']
    password = data['password']
    username = data['username']
    permission = data['permission']

    sql = '''
    INSERT INTO employees (first_name, last_name, password, username, permission) 
    VALUES (?, ?, ?, ?, ?)
    '''

    cursor.execute(sql, (first_name, last_name, password, username, permission))

def edit_customer(cursor, data, time_now):
    customer_number = data['customerSearchField']
    sql = '''
    UPDATE customers SET last_checked_date = ? WHERE customer_id = ?
    '''
    cursor.execute(sql, (time_now, customer_number))

def add_order(cursor, data, employee_id, time_now, company_id=None):
    date_issued = data['dateIssued']
    amount = data['amount']
    check_number = data['checkNumber']
    customer_number = data['customerSearchField']
    uuid = data['uuid']
    base64 = data['base64']
    amount_issued = data['amountIssued']

    if not company_id:
        company_id = data['companyId']

    sql = '''
    INSERT INTO ORDERS 
    (
      order_uuid, customer_id, check_number, date_check_issued, amount, 
      check_photo, employee_id, order_create_date, amount_issued, company_id
    )
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    cursor.execute(sql, (uuid, customer_number, check_number, date_issued, amount,
                         base64, employee_id, time_now, amount_issued, company_id))

def add_customer(cursor, data, employee_id, time_now):
    first_name = data['first_name']
    last_name = data['last_name']
    customer_uuid = data['uuid']
    address = data['address']
    license_number = data['license_number']
    phone_number = data['phoneNumber']
    customer_photo = data['customer_base64']
    customer_license_photo = data['license_base64']
    phone_number = phone_number.replace('-', '').replace(')', '').replace('.', '').replace('+', '').replace('(', '')

    sql = '''
    INSERT INTO CUSTOMERS 
    (
      first_name, last_name, customer_uuid, phone_number, address, license_number, 
      customer_photo, customer_license_photo, employee_id, creation_date
    )
    VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    cursor.execute(sql, (first_name, last_name, customer_uuid, phone_number, address,
                         license_number, customer_photo, customer_license_photo,
                         employee_id, time_now))

def add_company(cursor, data, employee_id, time_now):
    company = data['company'].lower()
    company_address = data['company_address']
    company_phone = data['company_phone']

    select_sql = '''
    SELECT company_id FROM companies WHERE lower(name) = ?
    '''
    insert_sql = '''
    INSERT INTO companies (name, address, phone_number, employee_id, creation_date) 
    VALUES (?, ?, ?, ?, ?)
    '''
    update_sql = '''
    UPDATE companies SET address = ?, phone_number = ?, employee_id = ? WHERE company_id = ?
    '''

    cursor.execute(select_sql, (company,))
    count = cursor.fetchone()

    if not count:
        cursor.execute(insert_sql, (company, company_address, company_phone, employee_id, time_now))
        new_company_id = cursor.lastrowid
        return new_company_id
    else:
        cursor.execute(update_sql, (company_address, company_phone, employee_id, count[0]))
        return count[0]


# import sqlite3
#
# def add_user(cursor, data):
#     first_name = data ['firstName']
#     last_name = data['lastName']
#     password = data['password']
#     username = data['username']
#     permission = data['permission']
#
#     sql = f'''
#     INSERT INTO employees ( first_name, last_name, password, username, permission) values
#     ( '{first_name}', '{last_name}', '{password}', '{username}', '{permission}')
#
#     '''
#
#     cursor.execute(sql)
#
# def edit_customer(cursor, data, time_now):
#     customer_number = data['customerSearchField']
#     sql = f'''
#     update customers set last_checked_date = '{time_now}' where customer_id = {customer_number}
#     '''
#     cursor.execute(sql)
#
#
# def add_order(cursor, data, employee_id, time_now, company_id=None):
#     # company = data['company']
#     date_issued = data['dateIssued']
#     amount = data['amount']
#     # account_number = data['accountNumber']
#     check_number = data['checkNumber']
#     customer_number = data['customerSearchField']
#     uuid = data['uuid']
#     base64 = data['base64']
#     amount_issued = data['amountIssued']
#
#     if not company_id:
#         company_id = data['companyId']
#
#     print(company_id)
#
#     sql = f'''
#     INSERT INTO ORDERS
#     (
#       order_uuid,
#       customer_id,
#       check_number,
#       date_check_issued,
#       amount,
#       check_photo,
#       employee_id,
#       order_create_date,
#       amount_issued,
#       company_id
#     )
#     values
#     (
#      '{uuid}',
#      '{customer_number}',
#      '{check_number}',
#      '{date_issued}',
#      {amount},
#      '{base64}',
#      {employee_id},
#      '{time_now}',
#      {amount_issued},
#      {company_id}
#     )
#     '''
#
#     cursor.execute(sql)
#
#
# def add_customer(cursor, data, employee_id, time_now):
#     first_name = data['first_name']
#     last_name = data['last_name']
#     customer_uuid = data['uuid']
#     address = data['address']
#     license_number = data['license_number']
#     phone_number = data['phoneNumber']
#     customer_photo = data['customer_base64']
#     customer_license_photo = data['license_base64']
#     phone_number = phone_number.replace('-','').replace(')','').replace('.', '').replace('+','').replace('(','')
#
#     sql = f'''
#     INSERT INTO CUSTOMERS
#     (
#       first_name,
#       last_name,
#       customer_uuid,
#       phone_number,
#       address,
#       license_number,
#       customer_photo,
#       customer_license_photo,
#       employee_id,
#       creation_date
#     )
#     values
#     (
#      '{first_name}',
#      '{last_name}',
#      '{customer_uuid}',
#      '{phone_number}',
#      '{address}',
#      '{license_number}',
#      '{customer_photo}',
#      '{customer_license_photo}',
#      {employee_id},
#      '{time_now}'
#     )
#     '''
#
#     cursor.execute(sql)
#
#
# def add_company(cursor, data, employee_id, time_now):
#     company = data['company'].lower()
#     company_address = data['company_address']
#     company_phone = data['company_phone']
#
#     sql = f'''
#     select company_id from companies where lower(name) = '{company}'
#     '''
#
#     insert_sql = f'''
#     insert into companies
#     (
#     name,
#     address,
#     phone_number,
#     employee_id,
#     creation_date )
#
#     values
#
#     ( '{company}',
#     '{company_address}',
#     '{company_phone}',
#       {employee_id},
#       '{time_now}' )
#     '''
#
#     cursor.execute(sql)
#     count = cursor.fetchone()
#
#     if not count:
#         cursor.execute(insert_sql)
#         new_company_id = cursor.lastrowid
#         return new_company_id
#
#     update_sql = f'''
#     update companies
#     set
#     address =  '{company_address}',
#     phone_number = '{company_phone}',
#     employee_id =  {employee_id}
#     where company_id = {count[0]}
#     '''
#     cursor.execute(update_sql)
#
#     return count[0]
