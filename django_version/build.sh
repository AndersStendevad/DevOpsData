#!/bin/bash
tag=${1:-latest}
docker build -t old-flask-minitwit:$tag .