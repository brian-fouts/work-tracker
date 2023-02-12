#!/bin/bash

python manage.py makemigrations user
python manage.py makemigrations project
python manage.py makemigrations work
python manage.py makemigrations worktracker
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable