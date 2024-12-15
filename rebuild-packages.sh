#!/bin/zsh -feu

# https://github.com/ionos-cloud/reprepro/blob/multiple-versions-debian/docs/recovery
# packages.db
# This file contains multiple databases, one for each target, containing
# the chunks from the Packages or Sources files, indexed by package name.

set -x

# What's the status of `dists'? Which one is better?
mkdir --parents ok
if [[ ! -d ok/dists ]]
then
    mv -vf dists ok/dists || : ignore
fi


# `db': we don't need it:
mkdir --parents db.backup
# what if it's already there:
mv -v db/packages.db db.backup/ || : ignore


# regenerate: from the dists
rm -fv db/packages.db

# this is a `secondary' index:
# rm db/packagenames.db
mv -v db/packagenames.db db.backup/ || : ignore


#
rm -vf db/references.db

# ===========================
# here we need `localreadd' ./conf/distributions
# and ./conf/updates
reprepro update sid
# populates lists/localreadd_sid_*
reprepro export
# ===========================


# fixme: others!
reprepro dumpunreferenced
#
reprepro rereference

rm -fv db/checksums.db
reprepro collectnewchecksums

#
reprepro dumpunreferenced
reprepro checkpool
reprepro check
