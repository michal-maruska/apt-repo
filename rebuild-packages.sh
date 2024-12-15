#!/bin/zsh -feu

# https://github.com/ionos-cloud/reprepro/blob/multiple-versions-debian/docs/recovery
# packages.db
# This file contains multiple databases, one for each target, containing
# the chunks from the Packages or Sources files, indexed by package name.

set -x
mkdir --parents ok
mv -vf dists ok/dists || : ignore

mkdir --parents db.backup

mv -v db/packages.db db.backup/ || : ignore
rm -fv db/packages.db
# this is a secondary index:
# rm db/packagenames.db
mv -v db/packagenames.db db.backup/ || : ignore


rm -vf db/references.db

reprepro update sid
# fixme: others!

#
reprepro dumpunreferenced

reprepro rereference

rm -fv db/checksums.db
reprepro collectnewchecksums


reprepro dumpunreferenced
