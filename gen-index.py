#!/usr/bin/env python3
"""gen-index.py ROOT: write index.html in every directory under ROOT,
plus <pkg>.deb.html (control fields + file list) for each .deb."""
import html, subprocess, sys, time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
HIDE_AT_ROOT = {"db", "conf", "incoming", ".git", ".github"}  # reprepro internals

PAGE = """<!doctype html><meta charset=utf-8>
<meta name=viewport content="width=device-width">
<title>{title}</title>
<style>body{{font:14px/1.5 ui-monospace,monospace;max-width:64rem;margin:2rem auto;padding:0 1rem}}
td{{padding:0 1.5rem 0 0}}td.r{{text-align:right}}pre{{overflow-x:auto}}</style>
<h1>{title}</h1>{body}
"""

def size(n):
    for u in "BKMG":
        if n < 1024 or u == "G":
            return f"{n:.0f}{u}" if u == "B" else f"{n:.1f}{u}"
        n /= 1024

def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout

def deb_page(deb: Path):
    body = (f'<p><a href="{quote(deb.name)}">download {html.escape(deb.name)}</a> '
            f'({size(deb.stat().st_size)})</p>'
            f'<h2>Control</h2><pre>{html.escape(run("dpkg-deb", "-f", str(deb)))}</pre>'
            f'<h2>Contents</h2><pre>{html.escape(run("dpkg-deb", "-c", str(deb)))}</pre>')
    out = deb.with_name(deb.name + ".html")
    out.write_text(PAGE.format(title=html.escape(deb.name), body=body))

def listing(d: Path):
    rel = d.relative_to(ROOT).as_posix()
    rows = []
    if d != ROOT:
        rows.append('<tr><td><a href="../">../</a></td><td></td><td></td><td></td></tr>')
    for p in sorted(d.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
        if (d == ROOT and p.name in HIDE_AT_ROOT) or p.name == "index.html" \
           or p.name.endswith(".deb.html"):
            continue
        st = p.stat()
        name = p.name + ("/" if p.is_dir() else "")
        info = (f'<a href="{quote(p.name)}.html">info</a>'
                if p.suffix == ".deb" else "")
        rows.append(
            f'<tr><td><a href="{quote(name)}">{html.escape(name)}</a></td>'
            f'<td class=r>{"-" if p.is_dir() else size(st.st_size)}</td>'
            f'<td>{time.strftime("%Y-%m-%d %H:%M", time.gmtime(st.st_mtime))}</td>'
            f'<td>{info}</td></tr>')
    title = "/" if rel == "." else f"/{rel}/"
    (d / "index.html").write_text(
        PAGE.format(title=html.escape(title), body=f"<table>{''.join(rows)}</table>"))

def walk(d: Path):
    for p in sorted(d.iterdir()):
        if d == ROOT and p.name in HIDE_AT_ROOT:
            continue
        if p.is_dir():
            walk(p)
        elif p.suffix == ".deb":
            deb_page(p)
    listing(d)

walk(ROOT)
