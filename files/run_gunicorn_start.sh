#!/bin/bash
NAME="medicos_dev"
DOMAIN="dev.medicosvoluntarios.pe"
PROJECTDIR=/var/www/$DOMAIN/htdocs
DJANGODIR=/var/www/$DOMAIN/htdocs/
SOCKFILE=/var/www/$DOMAIN/run/gunicorn.sock
LOGFILE=/var/www/$DOMAIN/logs/gunicorn.log
USER=ubuntu
GROUP=www-data
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=$NAME.development_settings
DJANGO_WSGI_MODULE=$NAME.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
source $PROJECTDIR/env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec $PROJECTDIR/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGFILE
