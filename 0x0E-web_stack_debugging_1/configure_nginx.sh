#!/bin/bash

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt update
    sudo apt install nginx -y
fi

# Start Nginx if not already running
if ! ps aux | grep -q "[n]ginx"; then
    echo "Nginx is not running. Starting Nginx..."
    sudo nginx
fi

# Check if Nginx is already configured to listen on port 80
if ! grep -q "listen 80;" /etc/nginx/sites-available/default; then
    # Add configuration to listen on port 80
    echo "Adding 'listen 80;' to Nginx configuration..."
    sudo sed -i 's/^\(\s*listen \)\(.*\)\(;.*\)$/\180;\2/' /etc/nginx/sites-available/default
    
    # Restart Nginx service to apply changes
    sudo nginx -s reload
fi

# Check if Nginx is listening on port 80
if ss -tln | grep ':80\b'; then
    echo "Nginx is configured to listen on port 80."
else
    echo "Failed to configure Nginx to listen on port 80."
fi

