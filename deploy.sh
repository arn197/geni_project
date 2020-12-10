# /usr/bin/sh


sudo apt update
sudo apt install apache2
sudo apt install libapache2-mod-wsgi-py3
sudo a2enmod wsgi

sudo mkdir /var/www/html/geni_project
cd ..
sudo mv geni_project /var/www/html/geni_project
cd /var/www/html/geni_project/geni_project

sudo apt install python3-pip
sudo apt install python3-venv
sudo apt install python3-flask
sudo pip3 install flask
sudo python3 -m venv venv
sudo cp geni_project.conf /etc/apache2/sites-available/.
sudo a2ensite geni_project
sudo a2dissite 000-default
sudo service apache2 restart
