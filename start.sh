#!/bin/sh

git pull origin master
echo 'LOAD ENV VARIABLES'
source ./.env

pipenv install --deploy

echo 'RUN MIGRATION'
# python manage.py collectstatic --no-input
pipenv run python manage.py migrate
pipenv run python manage.py compilemessages

echo 'Kill Atlas process'
pid=`ps ax | grep gunicorn | grep $ATLAS_PORT | awk '{split($0,a," "); print a[1]}' | head -n 1`
if [ -z "$pid" ]; then
  echo "no gunicorn deamon on port $ATLAS_PORT"
else
  kill $pid
  echo "killed gunicorn deamon on port $ATLAS_PORT"
fi

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