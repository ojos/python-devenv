#! /usr/bin/env sh
set -e

exec gunicorn -c /gunicorn.py core.wsgi:application
