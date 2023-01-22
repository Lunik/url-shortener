#!/bin/bash

rm -rf dist/
mkdir -p dist/

PYTHON_IMAGE="python"
PYTHON_VERSION=3.10-alpine # or 3.7, 3.8, ...
docker run \
  --rm \
  -v $(pwd):/app \
  --workdir /app \
  --platform linux/amd64 \
  $PYTHON_IMAGE:$PYTHON_VERSION \
  pip3 install --upgrade pip && pip3 install \
    . \
    --target ./dist/package

cp -r functions dist/

pushd dist/
zip -r release.zip functions/ package/
popd
