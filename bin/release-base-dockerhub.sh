#!/bin/bash

docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_API_KEY

VERSION=base-`git rev-parse --short HEAD`
echo "Building $VERSION"
docker build -f docker/base.Dockerfile -t base-dev:$VERSION .
docker tag base-dev:$VERSION mrdonbrown/code-video-generator-base:$VERSION

echo "Pushing $VERSION"
docker push mrdonbrown/code-video-generator-base:$VERSION