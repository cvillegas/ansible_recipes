#!/usr/bin/env bash
set -xe

rsync -avz --exclude=".env" --delete ~/$PROJECT_FOLDER $SERVER_USER@$SERVER_ADDRESS:~/$PROJECT_FOLDER
ssh -p22 $SERVER_USER@$SERVER_ADDRESS "cd ~/$PROJECT_FOLDER/; sh deploy/run.sh"
