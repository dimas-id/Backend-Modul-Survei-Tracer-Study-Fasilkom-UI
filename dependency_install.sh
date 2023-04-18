#!/bin/sh  

#---------------------dependency--------------------------------------------
apk add bash
apk add --virtual build-deps gcc python3-dev musl-dev
apk add curl
#---------- gcc -------------------------------------------------------------
apk add build-base
#-------------- psycopg2-----------------------------------------------------
apk update \
&& apk add gettext \
&& apk add postgresql-dev \
&& pip install psycopg2-binary==2.8.6 \
&& apk add --no-cache git

#-------------- pillow ------------------------------------------------------
apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev