#!/bin/bash

docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_API_KEY

VERSION=`python setup.py --version`
echo "Building $VERSION"
docker build -t code-dev:$VERSION --build-arg VERSION=$VERSION -f docker/Dockerfile .
docker tag code-dev:$VERSION mrdonbrown/code-video-generator:$VERSION
docker tag code-dev:$VERSION mrdonbrown/code-video-generator:latest

echo "Pushing $VERSION"
docker push mrdonbrown/code-video-generator:$VERSION
docker push mrdonbrown/code-video-generator:latest