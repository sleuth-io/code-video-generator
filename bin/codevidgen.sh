#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Usage: codevidgen.sh PYTHON_SCENE_FILE"
    exit 1
fi


if [ "x$(which docker)" == "x" ]; then
  echo "Error: Missing docker binary. Install docker and then try again."
  exit 1
fi


echo "Output will be stored in 'media'"
mkdir -p media

docker run --rm \
           -it \
  -v $PWD:/project \
  -w /project \
  mrdonbrown/code-video-generator \
  codevidgen \
  "$@"
