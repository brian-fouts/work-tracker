#!/bin/bash
python manage.py makemigrations
python manage.py makemigrations worktracker
python manage.py migrate
