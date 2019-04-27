#!/usr/bin/env sh
# tidak mau jalan pake ini

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn atlas.wsgi:application --bind 0.0.0.0:8000 --error-logfile error.log --workers 3
