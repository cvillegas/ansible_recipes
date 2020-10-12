#!/usr/bin/env bash
set -xe

cp ~/env-server ~/medicos-voluntarios/.env
cd ~/medicos-voluntarios
python manage.py migrate
python manage.py collectstatic
cd ~
sudo systemctl restart medicos
sudo systemctl restart nginx
