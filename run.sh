#!/usr/bin/env bash

uwsgi --socket :5000 --wsgi-file youtube.py --callable app --master --die-on-term --manage-script-name --stats :1717 --processes 4 --threads 2
    # --http-socket
