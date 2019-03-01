FROM python:3.6.7-slim

# Set environment varibles
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN pip3 install pipenv
# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN pipenv install --deploy --system

# Copy the current directory contents into the container at /app
COPY . /app
