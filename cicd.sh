rm -rf /home/ubuntu/flask_app/cicd

sudo mkdir -p /home/ubuntu/flask_app/cicd

cd /home/ubuntu/flask_app/cicd

git clone https://github.com/inolo/mbkcashchecking.git

cd mbkcashchecking


rm -rf /home/ubuntu/flask_app/cashchecking/templates

mv templates /home/ubuntu/flask_app/cashchecking/templates

rm /home/ubuntu/flask_app/cashchecking/cashchecking.py

mv cashchecking.py /home/ubuntu/flask_app/cashchecking/cashchecking.py

rm /home/ubuntu/flask_app/cashchecking/db_sql.py

mv db_sql.py /home/ubuntu/flask_app/cashchecking/db_sql.py

rm /home/ubuntu/flask_app/cashchecking/sql.py

mv sql.py /home/ubuntu/flask_app/cashchecking/sql.py

rm /home/ubuntu/flask_app/cashchecking/cicd.sh

mv cicd.sh /home/ubuntu/flask_app/cashchecking/cicd.sh

systemctl restart cashchecking.service

#testing note 1128111 please work

