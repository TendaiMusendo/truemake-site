# TrueMake website

Live at https://truemake.co.uk (GitHub Pages, branch `master`, root). Domain
setup notes in `DOMAIN-SETUP.md`.

## Pages

| File | Page |
|---|---|
| `src/pages/index.html` | Home |
| `src/pages/services.html` | Services |
| `src/pages/approach.html` | How we work |
| `src/pages/about.html` | About |
| `src/pages/contact.html` | Contact |

`src/layout.html` holds the shared styles, header, footer and script. Each page
file is the body only.

## Editing and building

Edit a page under `src/pages/` (or the layout), then rebuild every page:

```
python -I tools/build_site.py .
```

That writes `index.html`, `services.html`, `approach.html`, `about.html` and
`contact.html` at the root, each with the document skeleton, a
Content-Security-Policy carrying the inline script's hash, favicon and
metadata. Page titles and descriptions live in `PAGES` inside the build script.
Commit and push to `master`; Pages republishes in about a minute. Never edit
the root HTML files by hand.

## Logo

`brand/` holds the logo files. `tools/build_logo.py` regenerates them from
`tools/wordmark.json` (Bricolage Grotesque glyph outlines produced by
`tools/wordmark.py` from the font file; needs `pip install fonttools`):

```
python -I tools/build_logo.py tools/wordmark.json brand
```

Brand colour `#5E291D`; light tint `#D9A08C`; ink `#221A17`; stone `#F8F5F3`.
