FROM python:3.6.7-slim

# Set environment varibles
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install git because we need this to clone custom lib
RUN apt-get update && \
    apt-get install -y git gettext

# Set the working directory to /app
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
# -- Adding Pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# -- Install dependencies:
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
RUN pip install whitenoise
#RUN pipenv install --deploy

# Copy the current directory contents into the container at /app
COPY . /app

CMD ["./start.sh"]