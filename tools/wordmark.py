"""Render a word as SVG path data from a variable TTF at given axis values.
Usage: python -I wordmark.py <font.ttf> <text> <wght> <opsz>
Prints JSON: {"paths":[{"char":..,"d":..,"x":..}], "width":..., "upem":..., "ascender":..., "descender":...}
"""
import json, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

font_path, text, wght, opsz = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
vf = TTFont(font_path)
axes = {a.axisTag: a for a in vf["fvar"].axes}
loc = {"wght": wght}
if "opsz" in axes:
    loc["opsz"] = opsz
if "wdth" in axes:
    loc["wdth"] = 100
f = instantiateVariableFont(vf, loc)
glyphset = f.getGlyphSet()
cmap = f.getBestCmap()
hmtx = f["hmtx"]
upem = f["head"].unitsPerEm
# simple pair kerning from GPOS if a flat kern table exists; otherwise none
kern = {}
try:
    from fontTools.ttLib.tables import otTables  # noqa
    gpos = f["GPOS"].table
    for lookup in gpos.LookupList.Lookup:
        for st in lookup.SubTable:
            if getattr(st, "LookupType", lookup.LookupType) != 2:
                continue
            if st.Format == 1:
                cov = st.Coverage.glyphs
                for i, ps in enumerate(st.PairSet):
                    for pvr in ps.PairValueRecord:
                        v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, "XAdvance") else 0
                        if v:
                            kern[(cov[i], pvr.SecondGlyph)] = v
            elif st.Format == 2:
                cov = st.Coverage.glyphs
                c1 = st.ClassDef1.classDefs
                c2 = st.ClassDef2.classDefs
                for g1 in cov:
                    k1 = c1.get(g1, 0)
                    for g2 in cmap.values():
                        k2 = c2.get(g2, 0)
                        rec = st.Class1Record[k1].Class2Record[k2]
                        v = rec.Value1.XAdvance if rec.Value1 and hasattr(rec.Value1, "XAdvance") else 0
                        if v and (g1, g2) not in kern:
                            kern[(g1, g2)] = v
except Exception:
    pass

x = 0
out = []
prev = None
for ch in text:
    g = cmap[ord(ch)]
    if prev and (prev, g) in kern:
        x += kern[(prev, g)]
    pen = SVGPathPen(glyphset)
    glyphset[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))  # flip y for SVG
    out.append({"char": ch, "d": pen.getCommands(), "x": x})
    x += hmtx[g][0]
    prev = g
print(json.dumps({"paths": out, "width": x, "upem": upem,
                  "ascender": f["hhea"].ascent, "descender": f["hhea"].descent,
                  "capHeight": f["OS/2"].sCapHeight}))
