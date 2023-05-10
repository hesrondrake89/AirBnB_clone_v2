#!/usr/bin/env bash

# Update package list and install nginx
sudo apt-get update
sudo apt-get -y install nginx

# Allow HTTP traffic through firewall
sudo ufw allow 'Nginx HTTP'

# Create directory structure for web_static
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create test HTML file
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link to current release
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of web_static to ubuntu user
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx config to serve static content
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# Restart Nginx service
sudo service nginx restart
