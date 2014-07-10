#!/bin/sh
packagename=$1
version=$2

if [ $# != 2 ]; then
    echo "usage: $0 <packagename> <version>"
    exit 1
fi

rpmbuild -ba SPECS/${packagename}.spec
mock --buildsrpm --spec SPECS/${packagename}.spec --sources SOURCES --root epel-6-x86_64
mv /var/lib/mock/epel-6-x86_64/result/${packagename}-${version}.el6.src.rpm SRPMS/
mock --rebuild SRPMS/${packagename}-${version}.el6.src.rpm --root epel-6-x86_64
mv /var/lib/mock/epel-6-x86_64/result/${packagename}-${version}*.rpm RPMS/
ls -l SRPMS/${packagename}-${version}* RPMS/${packagename}-${version}*
