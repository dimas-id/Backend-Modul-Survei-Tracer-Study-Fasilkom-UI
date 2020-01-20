FROM python:3.6.7-slim

# Set environment varibles
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install git because we need this to clone custom lib
RUN apk update \
    && apk install -y git gettext \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# Set the working directory to /app
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip3 install pipenv

# -- Adding Pipfiles
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

# -- Install dependencies:
RUN pipenv install --dev --system

# Copy the current directory contents into the container at /app
COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
