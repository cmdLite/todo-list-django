#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python3 manage.py collectstatic --noinput --clear
