#!/bin/bash

make migrate        # Apply database migrations
make collectstatic  # Collect static files

echo Starting UWSGI.

exec /usr/sbin/uwsgi --ini $base_dir/conf/uwsgi.ini
