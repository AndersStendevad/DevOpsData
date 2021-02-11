#!/bin/bash
tag=${1:-latest}
docker run -p 5000:5000 old-flask-minitwit:$tag