#!/bin/bash
base_python_interpreter=""
project_domain=""
project_port=80
project_path=`pwd`

read -p "Python interpreter: " base_python_interpreter
read -p "Your domain/ip without protocol (for example, google.com): " project_domain
read -p "Your port: " project_port

`$base_python_interpreter -m venv env`
source env/bin/activate
pip3 install -r req.txt

sed -i "s~dbms_template_path~$project_path~g" nginx/site.conf systemd/gunicorn.service
sed -i "s~replace_domain~$project_domain~g" nginx/site.conf src/settings/settings.py
sed -i "s~80~$project_port~g" nginx/site.conf

# setup django
echo src/manage.py migrate
echo src/manage.py makemigrations
echo src/manage.py migrate

echo "Create superuser:"
echo src/manage.py createsuperuser

# autostart setup

sudo ln -s $project_path/nginx/site.conf /etc/nginx/sites-enabled/
sudo ln -s $project_path/systemd/gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo service nginx restart
