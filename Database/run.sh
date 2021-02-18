#!/bin/bash
tag=${1:-latest}
docker run -d --name mydb-$tag -p 6666:5432 db:$tag
