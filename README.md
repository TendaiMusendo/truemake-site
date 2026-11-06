# TrueMake website

Live at https://truemake.co.uk (GitHub Pages, branch `master`, root). Domain
setup notes in `DOMAIN-SETUP.md`.

## Editing the page

Edit `src/page.html` (the page body and styles, no `<html>`/`<head>` wrapper),
then rebuild `index.html`, which adds the document skeleton, the
Content-Security-Policy with the inline script's hash, favicon and metadata:

```
python -I tools/build_site.py src/page.html index.html
```

Commit and push to `master`; Pages republishes in about a minute. Never edit
`index.html` by hand: a changed inline script without a rebuilt hash is
blocked by the CSP.

## Logo

`brand/` holds the logo files. `tools/build_logo.py` regenerates them from
`tools/wordmark.json` (Bricolage Grotesque glyph outlines produced by
`tools/wordmark.py` from the font file; needs `pip install fonttools`):

```
python -I tools/build_logo.py tools/wordmark.json brand
```

Brand colour `#5E291D`; light tint `#D9A08C`; ink `#221A17`; stone `#F8F5F3`.
