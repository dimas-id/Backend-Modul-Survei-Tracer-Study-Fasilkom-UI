#!/bin/sh

if [ "$ATLAS_SQL_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $ATLAS_DB_HOST $ATLAS_DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

http_proxy=http://proxy.cs.ui.ac.id:8080
https_proxy=http://proxy.cs.ui.ac.id:8080

python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py compilemessages

exec "$@"