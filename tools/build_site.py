"""Wrap the artifact-format page into a hardened standalone index.html.
Usage: python -I build_site.py <src.html> <out/index.html>"""
import sys, re, hashlib, base64
src = open(sys.argv[1], encoding="utf-8").read()
src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n?', '', src)
scripts = re.findall(r'<script>(.*?)</script>', src, flags=re.S)
hashes = " ".join("'sha256-%s'" % base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() for s in scripts)
csp = ("default-src 'none'; "
       "script-src " + hashes + "; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; "
       "img-src 'self' data:; "
       "connect-src 'none'; form-action 'none'; base-uri 'none'; "
       "upgrade-insecure-requests")
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta http-equiv="Content-Security-Policy" content="%s">\n'
        '<meta name="referrer" content="strict-origin-when-cross-origin">\n'
        '<link rel="canonical" href="https://truemake.co.uk/">\n'
        '<link rel="icon" type="image/svg+xml" href="brand/favicon.svg">\n'
        '<meta property="og:title" content="TrueMake Consulting">\n'
        '<meta property="og:description" content="AI enablement and software consulting. We connect Claude to the systems your business already runs, train your team, and build the software in between.">\n'
        '<meta property="og:url" content="https://truemake.co.uk/">\n') % csp
body_start = src.index('<header>')
out = head + src[:body_start] + '</head>\n<body>\n' + src[body_start:] + '</body>\n</html>\n'
open(sys.argv[2], "w", encoding="utf-8", newline="\n").write(out)
print("scripts hashed:", len(scripts)); print("bytes:", len(out))
