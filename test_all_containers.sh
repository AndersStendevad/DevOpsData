#!/bin/bash
./build_all_images.sh
docker-compose down && docker-compose -f docker-compose.yaml up --remove-orphans -d  web_test api_test && docker-compose logs -f -t