#!/bin/bash
source /home/fsociety/coronabot/venv/bin/activate
#source /home/fsociety/coronabot/venv/bin/postactivate
exec gunicorn -c "/home/fsociety/coronabot/gunicorn_config.py" coronabot.wsgi
