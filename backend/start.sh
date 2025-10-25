#!/usr/bin/env bash

# Run migrations
python manage.py migrate --no-input

# Create test users (ignore if they already exist)
python manage.py create_test_users || true

# Start Gunicorn
gunicorn cryptolab.wsgi:application
