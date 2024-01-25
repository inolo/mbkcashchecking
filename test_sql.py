import sqlite3

def get_sqlite_connection():
    conn = sqlite3.connect('cashchecking.db')
    cur = conn.cursor()
    return conn, cur

company = 'aa'

sql = f'''
select address,phone_number from companies where name = '{company}'
'''



conn, curr = get_sqlite_connection()

curr.execute(sql)
count = curr.fetchone()


print(count)