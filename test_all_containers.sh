#!/bin/bash
docker-compose build \
&& \
docker-compose up -d\
&& \
docker-compose run web sh -c "python3 manage.py wait_for_db && python3 manage.py test --noinput" \
&& \
docker-compose run api sh -c "python3 manage.py wait_for_db && python3 manage.py test --noinput" \
&& \
docker-compose down
