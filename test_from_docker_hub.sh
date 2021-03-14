#!/bin/bash
git pull && \
docker-compose -f test-compose.yaml down --remove-orphans && \
docker rmi $(docker images -a -q)
docker-compose -f test-compose.yaml up -d --force-recreate
