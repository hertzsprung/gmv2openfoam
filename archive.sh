#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo 'Usage: ./archive.sh <version>'
    exit 1
fi
git archive --prefix gmv2openfoam-$1/ -o gmv2openfoam-$1.tar.gz $1
