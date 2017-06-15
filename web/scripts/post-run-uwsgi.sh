#!/bin/bash
echo "Running uwsgi script!";
sleep 5  # wait for server to start up
/usr/local/bin/uwsgi --http :8000 --wsgi-file /web/beats/wsgi.py  # start uwsgi
