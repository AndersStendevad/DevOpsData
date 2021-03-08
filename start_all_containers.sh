#!/bin/bash
./build_all_images.sh
docker-compose down && docker-compose -f docker-compose.yaml up --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --abort-on-container-exit --remove-orphans -d web api && docker-compose logs -f -t
