"""Compose TrueMake logo SVGs from wordmark.json. Usage: python -I build_logo.py <wordmark.json> <outdir>"""
import json, sys, os

data = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

OLIVE, OLIVE_LIGHT, INK, CREAM, STONE = "#5E291D", "#E0A48E", "#1C1917", "#FFF7F3", "#FCFBF9"

def mark(size=64, bg=OLIVE, tick=CREAM, rule=OLIVE_LIGHT, as_symbol=False):
    # A tick checked against a straight edge: "true" in the maker's sense.
    body = (
        f'<rect width="64" height="64" rx="14" fill="{bg}"/>'
        f'<path d="M35 14H51" stroke="{rule}" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M15 35L27 47L48 24" stroke="{tick}" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    )
    if as_symbol:
        return body
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}" role="img" aria-label="TrueMake mark">'
            + body + '</svg>')

def wordmark_paths(true_fill, make_fill):
    parts = []
    for p in data["paths"]:
        fill = true_fill if p["char"] in "True" and p["x"] < data["paths"][4]["x"] else make_fill
        parts.append(f'<path d="{p["d"]}" fill="{fill}"/>')
    return "".join(parts)

def lockup(true_fill, make_fill, bg, tick, rule):
    s = 0.07
    cap = data["capHeight"] * s           # ~46px
    baseline = 4 + (56 - cap) / 2 + cap   # mark spans y 4..60
    w = data["width"] * s
    total_w = 72 + w + 6
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.0f} 64" width="{total_w:.0f}" height="64" role="img" aria-label="TrueMake">'
            f'<g transform="translate(4 4) scale(0.875)">{mark(as_symbol=True, bg=bg, tick=tick, rule=rule)}</g>'
            f'<g transform="translate(72 {baseline:.2f}) scale({s})">{wordmark_paths(true_fill, make_fill)}</g>'
            '</svg>')

files = {
    "mark.svg": mark(),
    "favicon.svg": mark(),
    "logo.svg": lockup(OLIVE, INK, OLIVE, CREAM, OLIVE_LIGHT),
    "logo-dark.svg": lockup(OLIVE_LIGHT, STONE, OLIVE_LIGHT, INK, OLIVE),
    "logo-mono.svg": lockup(INK, INK, INK, STONE, STONE),
}
for name, svg in files.items():
    with open(os.path.join(out, name), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(name, len(svg), "bytes")

# a contact sheet for review
sheet = f"""<!doctype html><html><head><meta charset="utf-8"><title>TrueMake logo sheet</title>
<style>body{{margin:0;font-family:system-ui;color:{INK}}} .row{{display:grid;grid-template-columns:1fr 1fr;}} .cell{{padding:48px;display:grid;gap:24px;align-content:start}}
.light{{background:{STONE}}} .dark{{background:{INK};color:{STONE}}} small{{opacity:.6;font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
.marks{{display:flex;gap:24px;align-items:center}}</style></head><body>
<div class="row"><div class="cell light"><small>Lockup, light</small>{files['logo.svg']}<small>Mark at 64 / 32 / 16</small><div class="marks">{mark(64)}{mark(32)}{mark(16)}</div><small>Mono</small>{files['logo-mono.svg']}</div>
<div class="cell dark"><small>Lockup, dark</small>{files['logo-dark.svg']}<small>Mark on dark</small><div class="marks">{mark(64)}{mark(32)}{mark(16)}</div></div></div>
</body></html>"""
with open(os.path.join(out, "logo-sheet.html"), "w", encoding="utf-8") as fh:
    fh.write(sheet)
print("logo-sheet.html")
