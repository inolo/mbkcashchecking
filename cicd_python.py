import os
import subprocess
import logging


log_filename = '/var/log/cash_restart.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    filename=log_filename,
                    filemode='w',
                    force=True)

if os.path.exists('/home/ubuntu/service_restart.txt'):
    # return1 = subprocess.check_output(['sudo', '/usr/bin/python3','/home/ubuntu/flask_app/cashchecking/sql.py'])
    returned_value = subprocess.check_output(['sudo', '/usr/bin/systemctl', 'restart', 'cashchecking.service'])
    logging.info(f"{returned_value}")

os.remove('/home/ubuntu/service_restart.txt')

# new check check pls finally working