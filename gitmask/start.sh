#!/usr/bin/env bash
echo "Populate confd templates"
confd -onetime -backend env

echo "Starting fcgiwrap service..."
service fcgiwrap start

echo "Starting nginx daemon..."
nginx #-g "daemon off;"

echo "Enable the http endpoint"
ln -s /etc/nginx/sites-available/http.gitmask.conf /etc/nginx/sites-enabled/http.gitmask.conf

echo "Generate Letsencrypt SSL certificates"
cd "/srv/letsencrypt/" && ./letsencrypt.sh --cron

echo "Enable the https endpoint"
ln -s /etc/nginx/sites-available/https.gitmask.conf /etc/nginx/sites-enabled/https.gitmask.conf


tail -f /var/log/nginx/error.log -f /var/log/nginx/access.log -f /var/log/nginx/https.git.gitmask.com.log -f /var/log/nginx/http.git.gitmask.com.log