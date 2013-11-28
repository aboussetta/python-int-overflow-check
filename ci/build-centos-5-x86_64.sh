#!/bin/bash
set -x
set -e
sudo cp -u $WORKSPACE/packaging/mock-target-configs/centos-5-x86_64-epel-ius-pdb.cfg /etc/mock/
rm -rf /home/jenkins/packages/python-int-overflow-check-centos-5-x86_64
rm -rf $WORKSPACE/results
mkdir -p $WORKSPACE/results
cd /home/jenkins/packages
cp -a buildroot.clean python-int-overflow-check-centos-5-x86_64
cd $WORKSPACE
python setup.py sdist -d /home/jenkins/packages/python-int-overflow-check-centos-5-x86_64/SOURCES/
cp $WORKSPACE/packaging/SPECS/CentOS/python-int-overflow-check.spec /home/jenkins/packages/python-int-overflow-check-centos-5-x86_64/SPECS/
cd /home/jenkins/packages/python-int-overflow-check-centos-5-x86_64
rpmbuild -bs --nodeps --define "dist %{nil}" --define "_source_filedigest_algorithm md5" SPECS/python-int-overflow-check.spec 
for f in SRPMS/*.rpm; do mock -r centos-5-x86_64-epel rebuild $f --resultdir=$WORKSPACE/results ; done
