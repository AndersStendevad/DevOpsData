#!/bin/bash
./build_all_images.sh
docker-compose down && docker-compose -f docker-compose.yaml up --remove-orphans -d web api && docker-compose logs -f -t
