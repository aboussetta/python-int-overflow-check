#!/bin/bash
set -x
set -e
sudo apt-get install python-setuptools
rm -rf $WORKSPACE/result
mkdir -p $WORKSPACE/result
cd $WORKSPACE/debian-debian
git-buildpackage --git-builder="DIST=precise ARCH=amd64 pdebuild --buildresult ../result/" 2>&1 | tee ../build.log

