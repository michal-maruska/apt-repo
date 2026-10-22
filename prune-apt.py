#!/usr/bin/env python3
"""prune-apt.py [--keep N] [--apply] [BASEDIR]"""
import argparse, subprocess
from collections import defaultdict
from functools import cmp_to_key

ap = argparse.ArgumentParser()
ap.add_argument("base", nargs="?", default=".")
ap.add_argument("--keep", type=int, default=1)
ap.add_argument("--apply", action="store_true")
ap.add_argument("--confdir")

a = ap.parse_args()

def reprepro(*args, check=True):
    cmd = ["reprepro", "-b", a.base]
    if a.confdir:
        cmd += ["--confdir", a.confdir]
    return subprocess.run(cmd + list(args),
                          capture_output=True, text=True, check=check).stdout

def vcmp(x, y):
    if subprocess.run(["dpkg", "--compare-versions", x, "lt", y]).returncode == 0: return -1
    if subprocess.run(["dpkg", "--compare-versions", x, "gt", y]).returncode == 0: return 1
    return 0

# (codename, package, arch) -> [versions]
seen = defaultdict(set)
for line in reprepro("ls").splitlines():
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 4: continue
    pkg, ver, codename, archs = parts
    for arch in archs.split(","):
        seen[(codename, pkg, arch.strip())].add(ver)

for (codename, pkg, arch), vers in sorted(seen.items()):
    ordered = sorted(vers, key=cmp_to_key(vcmp), reverse=True)
    for old in ordered[a.keep:]:
        sel = ["-T", "dsc"] if arch == "source" else ["-A", arch]
        flt = f"Package (== {pkg}), Version (== {old})"
        print(f"{'REMOVE' if a.apply else 'would remove'} {codename} {pkg} {old} [{arch}]")
        if a.apply:
            reprepro(*sel, "removefilter", codename, flt)

if a.apply:
    reprepro("deleteunreferenced")
