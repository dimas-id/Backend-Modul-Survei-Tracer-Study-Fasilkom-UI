#!/usr/bin/env sh

source ./.env

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py compilemessages

gunicorn atlas.wsgi:application --bind 0.0.0.0:8000 --error-logfile error.log 
