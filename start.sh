#!/usr/bin/env bash
echo "Starting fcgiwrap service..."
service fcgiwrap start

echo "Starting nginx daemon..."
nginx -g "daemon off;"