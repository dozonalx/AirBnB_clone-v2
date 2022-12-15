#!/usr/bin/env bash
# This scripts sets up my web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo 'Holberton School' | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu /data/
sudo chgrp -R ubuntu /data/
# sudo sed -i "/server_name _;/ a\\\trewrite ^/redirect_me http://www.google.com permanent;" /etc/nginx/sites-available/default
# sudo sed -i '/server_name _;/a location /hbnb_static {alias /data/web_static/current; index index.html index.htm;}' /etc/nginx/sites-available/default
# sudo sed -i '/server_name _;/a error_page 404 /404.html; location = /404.html {root /var/www/error/;internal; }' /etc/nginx/sites-available/default
# sudo sed -i "/listen [::]:80 default_server;/a \n\tadd_header X-Served-By $HOSTNAME;" /etc/nginx/sites-available/default
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://google.com/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" | sudo tee /etc/nginx/sites-available/default
sudo service nginx restart
