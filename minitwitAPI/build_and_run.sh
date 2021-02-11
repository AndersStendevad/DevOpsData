#!/bin/bash

printf "=============\nBuilding the image\n=============\n\n"
timestamp=$(date +%Y%m%d%H%M%S)
./build.sh "$timestamp"
if [ $? -eq 0 ]; then
    printf "\n\n==============================================\nBuild successful, running the latest build\n==============================================\n\n"
    ./run.sh "$timestamp"
else
    echo "Something went wrong, check the previous error messages!"
fi