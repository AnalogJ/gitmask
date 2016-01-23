#!/usr/bin/env bash
echo "Populate confd templates"
confd -onetime -backend env

echo "Starting fcgiwrap service..."
service fcgiwrap start

echo "Enable the http endpoint"
ln -s /etc/nginx/sites-available/http.gitmask.conf /etc/nginx/sites-enabled/http.gitmask.conf

echo "Starting nginx service..."
service nginx start

echo "Generate Letsencrypt SSL certificates"
/srv/letsencrypt/letsencrypt.sh --cron

echo "Register Letsencrypt to run weekly"
crontab -l | { cat; echo "@weekly /srv/letsencrypt/letsencrypt.sh --cron"; } | crontab -

echo "Enable the https endpoint"
ln -s /etc/nginx/sites-available/https.gitmask.conf /etc/nginx/sites-enabled/https.gitmask.conf

echo "Reload nginx service..."
service nginx reload

tail -f /var/log/nginx/error.log -f /var/log/nginx/access.log -f /var/log/nginx/https.git.gitmask.com.log -f /var/log/nginx/http.git.gitmask.com.log