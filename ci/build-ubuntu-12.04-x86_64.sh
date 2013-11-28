#!/bin/bash
set -x
set -e
sudo apt-get install python-setuptools
cd $WORKSPACE

# clean up existing old files
rm -rf *.log
rm -rf *.build
rm -rf *.changes
rm -rf *.tar.gz
rm -rf *.dsc
rm -rf *.deb
rm -rf $WORKSPACE/result

mkdir -p $WORKSPACE/result
cd $WORKSPACE/debian-debian
git-buildpackage --git-builder="DIST=precise ARCH=amd64 pdebuild --buildresult ../result/" 2>&1 | tee ../build.log

