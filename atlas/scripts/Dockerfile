# pull official base image
FROM python:3.6.8-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add gettext \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2-binary==2.8.6 \
    && apk del build-deps \
    && apk add --no-cache git

# install dependencies
RUN pip install --upgrade pip
RUN pip3 install pipenv

# -- Adding Pipfiles
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

# -- Install dependencies:
RUN pipenv install --system --skip-lock

# COPY script-test.py /code/script-test.py
RUN echo "00 00 01 */6 * python /app/manage.py runscript bright-data-script" | crontab -
# CMD ["crond","-f"]
