import shutil
import os 
import time

base_dir = '/home/ubuntu/flask_app/cashchecking'

files = os.listdir(base_dir)

time_now = str(time.time())
os.mkdir(f'{base_dir}/backup/{time_now}')


destination_dir = f'/home/ubuntu/flask_app/cashchecking/backup/{time_now}'

move_list = ['cashchecking.py','db_sql.py','dml_sql.py', 'sql.py']


for file in files:
    if file in move_list:
        shutil.move(f'{base_dir}/{file}', f'{destination_dir}/{file}')
shutil.move(f'{base_dir}/templates', f'{destination_dir}/templates')

