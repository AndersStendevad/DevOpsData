#!/bin/bash
tag=${1:-latest}
docker build -t db:$tag .
