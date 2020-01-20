FROM nginx:1.17.7-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY app.conf /etc/nginx/conf.d

ENV APP=/app
RUN mkdir $APP
RUN mkdir $APP/staticfiles
RUN mkdir $APP/mediafiles
