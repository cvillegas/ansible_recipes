#!/bin/bash

VENV="medicos_dev"
REPO="dev.medicosvoluntarios.git"
DOMAIN=dev.medicosvoluntarios.pe
PROJECTDIR=/var/www/$DOMAIN
DJANGODIR=$PROJECTDIR/htdocs
REPODIR=/var/git/repo/$REPO
HTDOCSDIR=/var/www/$DOMAIN/htdocs
USER=ubuntu
GROUP=www-data

branch=master
echo "Checking out files from branch $branch in $REPODIR to $HTDOCSDIR..."
git --work-tree=$HTDOCSDIR --git-dir=$REPODIR checkout -f $branch

# Go to project folder
echo "Changing directory to $DJANGODIR..."
cd $DJANGODIR

echo "Looking for env in $DJANGODIR... "
if [ ! -d env ]; then
  echo "Linking virtual environment..."
  ln -s ~/.pyenv/versions/$VENV $DJANGODIR/env
else
  echo "Virtual environment already linked"
fi

# Make run dir
if [ ! -d $PROJECTDIR/run ]; then
  mkdir $PROJECTDIR/run
fi

sudo chown -hR $USER:$GROUP *

echo "Activating virtual environment..."
source env/bin/activate

echo "Upgrading pip..."
$DJANGODIR/env/bin/pip install --upgrade pip

$DJANGODIR/env/bin/pip install -r requirements.txt

cd $DJANGODIR

$DJANGODIR/env/bin/python manage.py migrate
$DJANGODIR/env/bin/python manage.py collectstatic --noinput

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart medicos_dev_gunicorn