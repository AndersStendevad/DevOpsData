#!/bin/bash
docker-compose -f deploy-compose.yaml down && \
docker rmi $(docker images -a -q) && \
docker-compose -f deploy-compose.yaml up -d --force-recreate
