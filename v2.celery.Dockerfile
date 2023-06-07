FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --src /usr/local/src

COPY . /app

CMD ["celery", "-A", "atlas.apps.email_blaster", "worker", "-l", "INFO"]














