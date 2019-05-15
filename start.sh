#!/usr/bin/env sh

git pull origin master

echo 'LOAD ENV VARIABLES'
source ./.env

pipenv install --deploy

echo 'RUN MIGRATION'
# python manage.py collectstatic --no-input
pipenv run python manage.py migrate
pipenv run python manage.py compilemessages

echo 'RUN GUNICORN BIND ON 8000'
nohup pipenv run gunicorn atlas.wsgi:application \
	--bind 0.0.0.0:8000 \
	--access-logfile - \
	--error-logfile error.log \
	--workers=3 \
	> /dev/null & echo $(($!+1)) > atlas.pid

echo 'RUN RQWORKER'
nohup pipenv run python manage.py rqworker > /dev/null & echo $(($!+1)) > atlas_rq.pid

echo 'ATLAS DEPLOYMENT SUCCESS'