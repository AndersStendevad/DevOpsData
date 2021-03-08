#!/bin/bash
docker-compose build && \
docker-compose up \
--abort-on-container-exit \
--exit-code-from api_test && \
docker-compose down

