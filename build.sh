#!/bin/bash

rm -rf dist/
mkdir -p dist/

PYTHON_VERSION=3.10 # or 3.7, 3.8, ...
docker run \
  --rm \
  -v $(pwd):/app \
  --workdir /app \
  rg.fr-par.scw.cloud/scwfunctionsruntimes-public/python-dep:$PYTHON_VERSION \
  pip install --upgrade pip && pip install \
    . \
    --target ./dist/package

cp -r functions dist/

pushd dist/
zip -r release.zip functions/ package/
popd