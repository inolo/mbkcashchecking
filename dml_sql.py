import sqlite3


def add_order(cursor, data, employee_id):
    company = data['company']
    date_issued = data['dateIssued']
    amount = data['amount']
    account_number = data['accountNumber']
    check_number = data['checkNumber']
    customer_number = data['customerNumber']
    uuid = data['uuid']
    base64 = data['base64']
    # cust_uuid = data['customer_uuid']

    sql = f'''
    INSERT INTO ORDERS 
    (
      order_uuid,
      customer_id,
      customer_uuid,
      date_check_issued,
      company,
      check_number,
      check_account_number,
      amount, 
      check_photo,
      employee_id
    )
    values 
    (
     '{uuid}',
     '{customer_number}',
     1111,
     '{date_issued}',
     '{company}',
     {check_number},
     '{account_number}',
     {amount},
     '{base64}',
     {employee_id}
    )
    '''

    cursor.execute(sql)
