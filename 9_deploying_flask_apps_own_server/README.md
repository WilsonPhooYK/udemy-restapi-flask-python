# Instructions for AWS

1. Start at AWS Management Console
2. Launch a virtual machine
3. Step 1: Choose an Amazon Machine Image (AMI) - Free tier - Ubuntu Server 16.04 LTS (HVM), SSD Volume Type
4. Default the rest of the settings and create instance
5. Install PuTTY and follow instruction to connect to ubuntu instance `https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html`
6. PuTTY hostname: ubuntu@ec2-13-213-61-24.ap-southeast-1.compute.amazonaws.com
7. Once in SSH run: `sudo apt-get update`, `sudo apt-get install libpcre3 libpcre3-dev` first.
8. More dependencies: `sudo apt-get install postgresql postgresql-contrib`
9. Login as postgres user: `sudo -i -u postgres`
10. Create new user: `sudo -i -u root`, `adduser wilson`
11. Follow this to add ssh credentials to new user: `https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/`. Go to PuTTY Key Generator, load the .pem file. Go to `cd .ssh`. `nano authorized_keys`. Copy `ssh-rsa .....3INCZ` and add ` wilson` behind. Ctrl-O + Ctrl-X to save
11. Set privileges: `visudo`. Under `root ALL=(ALL:ALL) ALL` add `wilson ALL=(ALL:ALL) ALL`. Ctrl-O + Ctrl-X to save
12. Set authentication: `vi /etc/ssh/sshd_config`, set `PermitRootLogin no`. End of file add `AllowUsers wilson`. `:wq` to save and quit
13. Refresh and use the new configuration: `service sshd reload`

# postgresql configuration
1. Create postgres sql user: `sudo su`, `sudo -i -u postgres`, `createuser wilson -P` - Must be same name as login user.
2. Create db for wilson: `createdb wilson`
3. Verify db exists for wilson: `exit`, `exit` to go back to `wilson`. `psql`, `\conninfo`
4. Set postgresql configuration file as root: `sudo vi /etc/postgresql/12/main/pg_hba.conf`. Update `local is for Unix domain socket connections only`, `peer` to `md5`

# nginx
1. Install: `sudo apt-get install nginx`
2. Let nginx have access through the firewall: `sudo ufw status`, `sudo ufw enable`, `sudo ufw allow 'Nginx HTTP'`
3. Important: `sudo ufw allow ssh` so we do not get locked out of server
4. Check if nginx is running: `systemctl status nginx`
5. Some other nginx commands: `systemctl (start|stop|restart) nginx`
6. nginx configuration: `sudo vi /etc/nginx/sites-available/items-rest.conf`
```
server {
listen 80; // Set port
real_ip_header X-Forwarded-For; // Forward ip of requester to flask app
set_real_ip_from 127.0.0.1; // Set it is really coming from 127.0.0.1
server_name localhost;

location / { // Whenever someone access the root location of server, redirect to flask app
include uwsgi_params;
uwsgi_pass unix:/var/www/html/items-rest/socket.sock; // Pass all params to sock file, which is a connection point between Flask and nginx
uwsgi_modifier1 30; // Tells thread when to die when they become blocked
}

error_page 404 /404.html; // Redirect to 404 page if 404
location = /404.html { // When location is exactly 404.html, do the following
root /usr/share/nginx/html; // Server 404.html from here
}

error_page 500 502 503 504 /50x.html;
location = /50x.html {
root /usr/share/nginx/html;
}
}
```
7. Enable the config: `sudo ln -s /etc/nginx/sites-available/items-rest.conf /etc/nginx/sites-enabled/`
8. Make folder where application is going to live: `sudo mkdir /var/www/html/items-rest`, `sudo chown wilson:wilson /var/www/html/items-rest`

# Pull project
1. `cd /var/www/html/items-rest`, `git clone https://github.com/WilsonPhooYK/udemy-restapi-flask-python-section-8.git .`
2. Create logs for our app: `mkdir log`
3. `sudo apt-get install python3-pip python3.9-dev python3.9 libpq-dev`. `libpq-dev` - To run psycopg2
4. `python3.9 -m pip install virtualenv`
5. Create new python virtualenv: `python3.9 -m virtualenv venv --python=python3.9`
6. Run virtualenv: `source venv/bin/activate`
7. Disable virtualenv: `source venv/bin/deactivate`
8. Install requirements: `python3.9 -m pip install -r requirements.txt`

# Create ubuntu service
1. `sudo vi /etc/systemd/system/uwsgi_items_rest.service`
```
[Unit] // Section
Description=uWSGI items rest

[Service]
Environment=DATABASE_URI=postgres://wilson:PASSWORD@localhost:5432/wilson
ExecStart=/var/www/html/items-rest/venv/bin/uwsgi --master --emperor /var/www/html/items-rest/uwsgi.ini --die-on-term --uid wilson --gid wilson --logto /var/www/html/items-rest/log/emperor.log  // Use master process, if crash take python code also, runs as wilson
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target // Starts service when server boots up
```
2. Change settings: `vi uwsgi.ini` for uwsgi how to run our python code
```
base = /var/www/html/items-rest
app = run
module = %(app) // loaded app module

home = %(base)/venv // home of uwsgi process
pythonpath = %(base) // where python project begins

socket = %(base)/socket.sock

chmod-socket = 777 // permission of socket to 777 - anybody can access socket file

processes = 8

threads = 8

harakiri = 15 // after 15s destroy and create new one

callable = app // app in run.py file

logto = /var/www/html/items-rest/log/%n.log // &n = uwsig
```

# Delete default nging configuration
1. `sudo rm /etc/nginx/sites-enabled/default`
2. `sudo systemctl reload nginx`
3. `sudo systemctl restart nginx`

# Extra AWS stuffs
1. The port 80 was closed at the AWS EC2 instance. Just go to Security Group > launch wizard > edit inbound rules > add a new rule of type 'HTTP' and source 'anywhere'

# Run app
1. `sudo systemctl start uwsgi_items_rest`. Run the service ExecStart, which runs uwsgi and look at uwsgi.ini file and run the flask app and create the socket file and commnicate with nginx
2. See logs: `vi log/uwsgi.log`
