import os
import shutil
import subprocess

# Define paths
base_path = '/home/ubuntu/flask_app'
cicd_path = os.path.join(base_path, 'cicd')
cashchecking_path = os.path.join(base_path, 'cashchecking')
repo_url = 'https://github.com/inolo/mbkcashchecking.git'

# Remove cicd directory if it exists
if os.path.exists(cicd_path):
    shutil.rmtree(cicd_path)

# Create cicd directory
os.makedirs(cicd_path, exist_ok=True)

# Clone the git repository
subprocess.run(['git', 'clone', repo_url], cwd=cicd_path)

# Define paths within the cloned repo
repo_dir = os.path.join(cicd_path, 'mbkcashchecking')

# List of files to move
files_to_move = ['templates', 'cashchecking.py', 'db_sql.py', 'sql.py', 'cicd.sh', 'cicd_python.py']

# Move the files
for file in files_to_move:
    src = os.path.join(repo_dir, file)
    dest = os.path.join(cashchecking_path, file)
    if os.path.exists(dest):
        if os.path.isdir(dest):
            shutil.rmtree(dest)
        else:
            os.remove(dest)
    shutil.move(src, dest)

# Set permissions for cicd.sh
os.chmod(os.path.join(cashchecking_path, 'cicd.sh'), 0o777)

# Restart the service
subprocess.run(['sudo', 'systemctl', 'restart', 'cashchecking.service'])
