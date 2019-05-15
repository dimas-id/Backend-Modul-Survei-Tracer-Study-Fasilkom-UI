#!/bin/sh

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo 'LOAD ENV VARIABLES'
		source ./.env

    echo 'INSTALL DEPENDENCIES'
		pipenv install --deploy

		echo 'RUN MIGRATION'
		# python manage.py collectstatic --no-input
		pipenv run python manage.py migrate
		pipenv run python manage.py compilemessages

		echo 'SIGHUP Atlas process'
		kill -HUP $(<"/home/wisnuprama/iluni12/b3-atlas/atlas.pid")

		echo 'SIGHUP Atlas RQWorker process'
		kill -HUP $(<"/home/wisnuprama/iluni12/b3-atlas/atlas_rq.pid")

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
fi
