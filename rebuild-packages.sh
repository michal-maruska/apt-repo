#!/bin/zsh -feu

# https://github.com/ionos-cloud/reprepro/blob/multiple-versions-debian/docs/recovery
# packages.db
# This file contains multiple databases, one for each target, containing
# the chunks from the Packages or Sources files, indexed by package name.

mv dists dists.ok

