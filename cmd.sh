#!/bin/bash
set -e

cd /app

cat >> /etc/cron.d/magic-cron <<EOL
SHELL=/bin/bash
BASH_ENV=/app/cron.env
$CRON_INTERVAL /app/cron.sh
EOL
chmod 0644 /etc/cron.d/magic-cron
crontab /etc/cron.d/magic-cron

printenv > cron.env

echo "Starting cron in foreground"
cron -f
