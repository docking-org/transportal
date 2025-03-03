#! /bin/bash

set -m 

python manage.py runserver 0.0.0.0:8123

fg %1