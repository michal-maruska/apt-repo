#!/usr/bin/env python3
"""prune-apt.py [--keep N] [--apply] [--dist CODENAME ...]
Uses REPREPRO_BASE_DIR / REPREPRO_CONFIG_DIR from the environment."""
import argparse, re, subprocess
from collections import defaultdict
from functools import cmp_to_key

ap = argparse.ArgumentParser()
ap.add_argument("--keep", type=int, default=1)
ap.add_argument("--apply", action="store_true")
ap.add_argument("--dist", action="append", default=None)
a = ap.parse_args()
dists = a.dist or ["sid"]

def reprepro(*args):
    return subprocess.run(["reprepro", *args], capture_output=True,
                          text=True, check=True).stdout

def vcmp(x, y):
    for op, r in (("lt", -1), ("gt", 1)):
        if subprocess.run(["dpkg", "--compare-versions", x, op, y]).returncode == 0:
            return r
    return 0

LINE = re.compile(r"^(?:\w+\|)?[^|]+\|[^|]+\|([^:]+): (\S+) (\S+)$")

for dist in dists:
    seen = defaultdict(set)                       # (pkg, arch) -> versions
    for line in reprepro("list", dist).splitlines():
        m = LINE.match(line)
        if m:
            arch, pkg, ver = m.groups()
            seen[(pkg, arch)].add(ver)

    for (pkg, arch), vers in sorted(seen.items()):
        ordered = sorted(vers, key=cmp_to_key(vcmp), reverse=True)
        for old in ordered[a.keep:]:
            print(f"{'REMOVE' if a.apply else 'would remove'} {dist} {pkg} {old} [{arch}]")
            if a.apply:
                sel = ["-T", "dsc"] if arch == "source" else ["-A", arch]
                reprepro(*sel, "removefilter", dist,
                         f"Package (== {pkg}), Version (== {old})")

if a.apply:
    reprepro("deleteunreferenced")
