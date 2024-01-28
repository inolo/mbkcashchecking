#!/usr/bin/bash

sudo rm -rf /home/ubuntu/flask_app/cicd

sudo mkdir -p /home/ubuntu/flask_app/cicd

cd /home/ubuntu/flask_app/cicd
#
git clone https://github.com/inolo/mbkcashchecking.git
#
cd mbkcashchecking
#
#
sudo rm -rf /home/ubuntu/flask_app/cashchecking/templates
#
sudo mv templates /home/ubuntu/flask_app/cashchecking/templates
#
sudo rm /home/ubuntu/flask_app/cashchecking/cashchecking.py
#
sudo mv cashchecking.py /home/ubuntu/flask_app/cashchecking/cashchecking.py

sudo rm /home/ubuntu/flask_app/cashchecking/db_sql.py

sudo mv db_sql.py /home/ubuntu/flask_app/cashchecking/db_sql.py

sudo rm /home/ubuntu/flask_app/cashchecking/dml_sql.py

sudo mv db_sql.py /home/ubuntu/flask_app/cashchecking/dml_sql.py

sudo rm /home/ubuntu/flask_app/cashchecking/sql.py

sudo mv sql.py /home/ubuntu/flask_app/cashchecking/sql.py

sudo rm /home/ubuntu/flask_app/cashchecking/cicd.sh

sudo mv cicd.sh /home/ubuntu/flask_app/cashchecking/cicd.sh

sudo chmod 777 /home/ubuntu/flask_app/cashchecking/cicd.sh

sudo rm /home/ubuntu/flask_app/cashchecking/cicd_python.py

sudo mv cicd_python.py /home/ubuntu/flask_app/cashchecking/cicd_python.py


sudo touch /home/ubuntu/service_restart.txt

sudo /usr/bin/python3 /home/ubuntu/flask_app/cashchecking/sql.py

#testing note 1128111 please work now??///111111112132111aaaaatestaatesttry thisaa13131 new testaaasssaaa

