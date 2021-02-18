#!/bin/bash
. ./version.properties

VERSION=${version:-"unknown"}
NAME=${name:-"unknown"}

./build.sh

docker run -v `pwd`/sample_data.txt:/app/sample_data.txt -t --entrypoint="/bin/bash" ${NAME}:${VERSION} \
  -c 'cat /app/sample_data.txt | python -m matching_engine.app'

