#!/usr/bin/env bash
echo "Starting fcgiwrap service..."
service fcgiwrap start

echo "Starting nginx daemon..."
nginx -g "daemon off;"

#tail -f /var/log/nginx/error.log -f /var/log/nginx/access.log