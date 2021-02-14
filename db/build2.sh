#!/bin/bash
tag=${1:-latest}

rm -rf ${HOME}/postgres-data
mkdir ${HOME}/postgres-data

docker rm -f minitwit-postgres

docker run -d \
    --name minitwit-postgres \
    -e POSTGRES_PASSWORD=twit123! \
    -e POSTGRES_USER=superuser \
    -e POSTGRES_DB=tweets \
    -v ${HOME}/postgres-data/:/var/lib/postgresql/data \
    -p 5430:5430 \
    postgres:11.5