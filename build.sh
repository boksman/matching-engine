#!/bin/bash
. ./version.properties

VERSION=${version:-"unknown"}
NAME=${name:-"unknown"}

echo "Version: ${VERSION}"

CMD="docker build -t ${NAME}:${VERSION} -f Dockerfile ."
echo "${CMD}"
${CMD} || exit 1

echo "Build done"
