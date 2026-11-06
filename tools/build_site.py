"""Build the TrueMake site: src/layout.html + src/pages/*.html -> <name>.html at the repo root,
plus dist/artifact/index.html (artifact format, no document skeleton) for the claude.ai preview.
Usage: python -I tools/build_site.py <repo root>"""
import sys, os, re, hashlib, base64

root = sys.argv[1] if len(sys.argv) > 1 else "."
layout = open(os.path.join(root, "src", "layout.html"), encoding="utf-8").read()

PAGES = {
    "index":    ("TrueMake Consulting", "TrueMake is a consulting company for systems integration and AI enablement. We connect the platforms and sites your business runs, build by hand and with AI so your team tests a working version early, and support your team's AI adoption after go-live."),
    "services": ("Services · TrueMake", "Integration between your systems, AI enablement with support that stays, implementation and custom software by hand and with AI, and agents with a person in the loop."),
    "approach": ("How we work · TrueMake", "You click through a working version early, not at the end. Criteria before building, something to test early, sandbox and a signature before production, handover you can run without us."),
    "about":    ("About · TrueMake", "TrueMake is run by Tendai Musendo, who implements CRM and ERP systems hands-on and builds by hand and with AI. We are true to what we make."),
    "contact":  ("Contact · TrueMake", "Start with one process. Tell us the task that eats the most hours in your week and we will say plainly whether an agent or an integration can take it."),
}

def csp_for(html):
    scripts = re.findall(r'<script>(.*?)</script>', html, flags=re.S)
    hashes = " ".join("'sha256-%s'" % base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() for s in scripts)
    return ("default-src 'none'; script-src " + hashes + "; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; img-src 'self' data:; "
            "connect-src 'none'; form-action 'none'; base-uri 'none'; upgrade-insecure-requests")

def head(name, title, desc, csp):
    url = "https://truemake.co.uk/" + ("" if name == "index" else name + "/")
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta http-equiv="Content-Security-Policy" content="%s">\n'
            '<meta name="referrer" content="strict-origin-when-cross-origin">\n'
            '<link rel="canonical" href="%s">\n'
            '<link rel="icon" type="image/svg+xml" href="/brand/favicon.svg">\n'
            '<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n') % (csp, url, title, desc, url)

os.makedirs(os.path.join(root, "dist", "artifact"), exist_ok=True)
for name, (title, desc) in PAGES.items():
    content = open(os.path.join(root, "src", "pages", name + ".html"), encoding="utf-8").read()
    page = layout.replace("{{TITLE}}", title).replace("{{DESCRIPTION}}", desc).replace("{{CONTENT}}", content.rstrip("\n"))
    for other in PAGES:
        page = page.replace("{{ACTIVE_%s}}" % other, "active" if other == name else "")
    page = page.replace(' class=""', "")
    body_start = page.index("<header>")
    full = head(name, title, desc, csp_for(page)) + page[:body_start] + "</head>\n<body>\n" + page[body_start:] + "</body>\n</html>\n"
    # clean URLs: /services/ is served from services/index.html
    out_rel = "index.html" if name == "index" else os.path.join(name, "index.html")
    os.makedirs(os.path.dirname(os.path.join(root, out_rel)) or root, exist_ok=True)
    with open(os.path.join(root, out_rel), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(full)
    # artifact copies use flat relative links: the index without a skeleton, the others standalone
    art = page if name == "index" else full
    art = art.replace('href="/"', 'href="index.html"').replace('href="/brand/favicon.svg"', 'href="brand/favicon.svg"')
    for other in PAGES:
        art = art.replace('href="/%s/' % other, 'href="%s.html' % other)
    art_path = os.path.join(root, "dist", "artifact", name + ".html")
    with open(art_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(art)
    print("%-22s %6d bytes" % (out_rel, len(full)))
