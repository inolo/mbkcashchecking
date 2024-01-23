import sqlite3

def add_user(cursor, data):
    first_name = data ['firstName']
    last_name = data['lastName']
    password = data['password']
    username = data['username']
    permission = data['permission']

    sql = f'''
    INSERT INTO employees ( first_name, last_name, password, username, permission) values 
    ( '{first_name}', '{last_name}', '{password}', '{username}', '{permission}')
    
    '''

    cursor.execute(sql)

def edit_customer(cursor, data, time_now):
    customer_number = data['customerSearchField']
    sql = f'''
    update customers set last_checked_date = '{time_now}' where customer_id = {customer_number} 
    '''
    cursor.execute(sql)


def add_order(cursor, data, employee_id, time_now):
    # company = data['company']
    date_issued = data['dateIssued']
    amount = data['amount']
    # account_number = data['accountNumber']
    check_number = data['checkNumber']
    customer_number = data['customerSearchField']
    uuid = data['uuid']
    base64 = data['base64']

    sql = f'''
    INSERT INTO ORDERS 
    (
      order_uuid,
      customer_id,
      check_number,
      date_check_issued,
      amount, 
      check_photo,
      employee_id,
      order_create_date
    )
    values 
    (
     '{uuid}',
     '{customer_number}',
     '{check_number}',
     '{date_issued}',
     {amount},
     '{base64}',
     {employee_id},
     '{time_now}'
    )
    '''

    cursor.execute(sql)


def add_customer(cursor, data, employee_id, time_now):
    first_name = data['first_name']
    last_name = data['last_name']
    customer_uuid = data['uuid']
    address = data['address']
    license_number = data['license_number']
    phone_number = data['phoneNumber']
    customer_photo = data['customer_base64']
    customer_license_photo = data['license_base64']
    phone_number = phone_number.replace('-','').replace(')','').replace('.', '').replace('+','').replace('(','')

    sql = f'''
    INSERT INTO CUSTOMERS 
    (
      first_name,
      last_name,
      customer_uuid,
      phone_number,
      address,
      license_number, 
      customer_photo,
      customer_license_photo,
      employee_id,
      creation_date
    )
    values 
    (
     '{first_name}',
     '{last_name}',
     '{customer_uuid}',
     '{phone_number}',
     '{address}',
     '{license_number}',
     '{customer_photo}',
     '{customer_license_photo}',
     {employee_id},
     '{time_now}'
    )
    '''

    cursor.execute(sql)