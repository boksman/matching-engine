#!/bin/bash
. ./version.properties

VERSION=${version:-"unknown"}
NAME=${name:-"unknown"}

./build.sh

CMD="docker run -t ${NAME}:${VERSION} python -m pytest test"
echo "${CMD}"
${CMD} || exit 1

echo "done"
