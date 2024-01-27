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
    returned_value = subprocess.check_output('sudo systemctl restart cashchecking.service')
    logging.info(f"{returned_value}")

os.remove('/home/ubuntu/service_restart.txt')

# new check