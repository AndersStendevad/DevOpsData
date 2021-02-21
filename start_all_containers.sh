#!/bin/bash
./build_all_images.sh
docker-compose -f docker-compose.yaml up --remove-orphans
