#!/bin/bash
docker-compose -f deploy-compose.yaml down && \
docker-compose -f deploy-compose.yaml up -d --force-recreate
