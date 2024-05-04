#!/bin/bash

# Check if Nginx service is running
nginx_status=$(systemctl is-active nginx)
if [ "$nginx_status" != "active" ]; then
    echo "Nginx is not running. Starting Nginx..."
    sudo systemctl start nginx
else
    echo "Nginx is already running."
fi

# Check Nginx configuration
nginx_config="/etc/nginx/nginx.conf"
if [ -f "$nginx_config" ]; then
    listen_config=$(grep "listen 80;" "$nginx_config")
    if [ -z "$listen_config" ]; then
        echo "Adding 'listen 80;' to Nginx configuration..."
        echo "listen 80;" | sudo tee -a "$nginx_config" > /dev/null
        sudo systemctl reload nginx
    else
        echo "'listen 80;' already configured in Nginx."
    fi
else
    echo "Nginx configuration file not found."
fi

# Check if any process is already listening on port 80
port_80_status=$(sudo netstat -tuln | grep ":80 ")
if [ -n "$port_80_status" ]; then
    echo "Port 80 is already in use by another process:"
    echo "$port_80_status"
    exit 1
fi

echo "Nginx is configured to listen on port 80."

