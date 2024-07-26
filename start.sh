#!/bin/bash

# Start Celery worker
celery -A app.celery_config.make_celery worker --loglevel=info --concurrency=4 &

# Start Flask app with Gunicorn
exec gunicorn -b 0.0.0.0:5000 app.main:app
