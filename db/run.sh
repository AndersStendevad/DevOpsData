#!/bin/bash
tag=${1:-latest}
docker run -d --name mydb-$tag -p 5555:5432 db:$tag