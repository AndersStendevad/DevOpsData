#!/bin/bash
docker-compose build \
&& \
docker-compose up \
--exit-code-from api_test \
&& \
docker-compose down \
&& \
docker-compose up \
--exit-code-from web_test \
&& \
docker-compose down
