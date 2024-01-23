import sqlite3


def add_order(cursor, data, employee_id):
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
      employee_id
    )
    values 
    (
     '{uuid}',
     '{customer_number}',
     '{check_number}',
     '{date_issued}',
     {amount},
     '{base64}',
     {employee_id}
    )
    '''

    cursor.execute(sql)


def add_customer(cursor, data):
    first_name = data['first_name']
    last_name = data['last_name']
    customer_uuid = data['uuid']
    address = data['address']
    license_number = data['license_number']
    phone_number = data['phoneNumber']
    customer_photo = data['customer_base64']
    customer_license_photo = data['license_base64']

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
      customer_license_photo
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
     '{customer_license_photo}'
    )
    '''

    cursor.execute(sql)