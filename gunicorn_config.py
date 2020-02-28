command = '/home/fsociety/coronabot/venv/bin/gunicorn'
pythonpath = '/home/fsociety/coronabot'
bind = '127.0.0.1:8001'
workers = 1
user = 'fsociety'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=coronabot.settings'
