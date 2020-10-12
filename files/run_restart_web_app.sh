#!/bin/bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart medicos_dev_gunicorn

