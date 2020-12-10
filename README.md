

# Distributed Password Cracker WebApp
_____________________________________


The intention of this webapp is to brute force a 5 character from the md5 hash generated. 

1) To deploy the webapp, create a GENI slice. Use the rspec given in the repo `pwd-cracker-rspec.xml`

2) Once the nodes are available, clone this GitHub repo to all the nodes available

3) On all the worker nodes run `python3 workers.py <server host name> <port>` where serverhostname is **"server"** and port is set to **"6001"**

4) Login to the server node

5) Add the following information in the file geni_project.conf 
    On line 2: 'Servername   "Your server IP address"` 

6) Run the deployment script `deploy.sh`. This script does the following  
     1)  Adds the packages required (Flask) 
     2)  Installs apache2 and required wsgi libraries
     3)  Transfers files to /var/www/html public folder 
     4)  Configures the virtual host settings
     5)  Runs apache service

Your webserver is up and running! Open the browser and enter your server IP in the url.  
 
 Note :It's better to kill the port 6001 before running the management_service
with command `fuser -k 6001/tcp`


The link to our demo is here: https://drive.google.com/file/d/1FRWHhTjJ3a0sMqYxkwzPvF_QAhywVvxM/view?usp=sharing





     

     





