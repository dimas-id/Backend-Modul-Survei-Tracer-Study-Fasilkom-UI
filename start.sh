#!/bin/sh
git pull origin master
docker-compose -f docker-compose.prod.yml up -d --build