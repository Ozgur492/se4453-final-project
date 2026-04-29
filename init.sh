#!/bin/bash
set -e

# Inject Azure App Service environment variables into /etc/profile
# so they are available in SSH sessions (az webapp ssh)
eval $(printenv | sed -n "s/^\([^=]\+\)=\(.*\)$/export \1=\2/p" | sed 's/"/\\"/g' | sed '/=/s//="/' | sed 's/$/"/' >> /etc/profile)

# Start SSH daemon in the background
service ssh start

# Start gunicorn in the foreground (PID 1 via exec)
exec gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 app:app
