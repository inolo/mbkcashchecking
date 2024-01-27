import os
import subprocess


if os.path.exists('/home/ubuntu/service_restart.txt'):
    returned_value = subprocess.check_output('sudo systemctl restart cashchecking.sertvice', shell=True)

os.remove('/home/ubuntu/service_restart.txt')