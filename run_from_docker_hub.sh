#!/bin/bash
git pull && \
docker-compose -f deploy-compose.yaml down --remove-orphans && \
docker rmi $(docker images -a -q)
docker-compose -f deploy-compose.yaml up -d --force-recreate
