#!/bin/sh

# Process a lldpd tarball to remove proprietary source code.
#
# Yaakov Selkowitz <yselkowi@redhat.com> - 2021
#

SOURCE="$1"
NEW_SOURCE=`echo $SOURCE | sed 's/\.tar\.gz/-free&/'`
DIRECTORY=`echo $SOURCE | sed 's/\.tar\.gz//'`

error()
{
	MESSAGE=$1
	echo $MESSAGE
	exit 1
}

rm -rf $DIRECTORY
tar xzf $SOURCE || error "Cannot unpack $SOURCE"
pushd $DIRECTORY > /dev/null || error "Cannot open directory \"$DIRECTORY\""

echo "Remove proprietary source files"
find include/osx -type f -delete

echo

popd > /dev/null

tar czf $NEW_SOURCE $DIRECTORY
echo "$NEW_SOURCE is ready to use"
