#!/usr/bin/env python3
"""Swap bitmap logos for vectors.

The logos in assets/vec/ were exported as SVG from the FanZone Figma file (EyEm3J8Y3qrWV40vOPOkjV):
  bayern.svg      logo-FC_Bayernayern_Muenchen_RGB
  bundesliga.svg  logo-bundesliga_white_background (without its white square)
  juventus.svg    Juventus FC logo 1

Each PNG below is rebuilt as an SVG with the same framing as the PNG it replaces: the same
background (none, a circle or a rounded square), and the logo in the same box, measured from the PNG.
The SVGs are written to assets/vec/tiles/ and every reference in the app is pointed at them.
Logos that are bitmaps in Figma too (most team, league and competition logos, which the product
loads from a server) stay PNG.

Run last:  python3 tools/vector-assets.py FanZone.dc.html
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VEC = os.path.join(ROOT, 'assets', 'vec')
OUT = os.path.join(VEC, 'tiles')

# where the drawing sits inside each source SVG's viewBox: x0, y0, x1, y1
LOGOS = {
    'bayern':     (1.5, 1.5, 28.5, 28.5),
    'bundesliga': (3.41, 3.41, 34.2, 34.16),
    'juventus':   (0.0, 3.09, 13.26, 24.74),
}

# png path -> (logo, background, logo box as fractions of the tile: x0, y0, x1, y1)
#   background: None, ('circle', color) or ('rounded', color, radius as a fraction of the size)
TILES = {
    'assets/img/logo-bayern.png':          ('bayern', None, (0, 0, 1, 1)),
    'assets/poll/logo-fcb.png':            ('bayern', None, (0.023, 0.023, 0.977, 0.977)),
    'assets/profile/int-bayern.png':       ('bayern', ('circle', '#FFFFFF'), (0.069, 0.069, 0.931, 0.931)),
    'assets/profile/mw-bayern.png':        ('bayern', ('rounded', '#DC052D', 1 / 6), (0.15, 0.15, 0.85, 0.85)),
    'assets/mycard/tile-bayern.png':       ('bayern', ('rounded', '#DC052D', 1 / 6), (0.15, 0.15, 0.85, 0.85)),
    'assets/fixture/crest-bundesliga.png': ('bundesliga', ('circle', '#FFFFFF'), (0.188, 0.188, 0.812, 0.812)),
    'assets/profile/int-bundesliga.png':   ('bundesliga', ('circle', '#FFFFFF'), (0.181, 0.181, 0.819, 0.819)),
    'assets/others/int-bundesliga.png':    ('bundesliga', ('circle', '#FFFFFF'), (0.181, 0.181, 0.819, 0.819)),
    'assets/profile/mw-bundesliga.png':    ('bundesliga', ('rounded', '#FFFFFF', 1 / 6), (0.183, 0.192, 0.808, 0.817)),
    'assets/mycard/tile-bundesliga.png':   ('bundesliga', ('rounded', '#FFFFFF', 1 / 6), (0.183, 0.192, 0.808, 0.817)),
    'assets/img/logo-juventus.png':        ('juventus', None, (0, 0, 1, 1)),
    'assets/mycard/tile-juventus.png':     ('juventus', ('rounded', '#FFFFFF', 1 / 6), (0.317, 0.275, 0.65, 0.825)),
}

def logo_inner(name):
    s = open(os.path.join(VEC, name + '.svg'), encoding='utf-8').read()
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    # ids must be unique once nested; prefix them with the logo name
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{name}-{m.group(1)}"', body)
    body = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{name}-{m.group(1)})', body)
    return body

def build(png, logo, bg, box):
    S = 120.0  # tile units; the SVG scales to whatever size the page gives it
    x0, y0, x1, y1 = LOGOS[logo]
    lw, lh = x1 - x0, y1 - y0
    bx0, by0, bx1, by1 = box[0] * S, box[1] * S, box[2] * S, box[3] * S
    bw, bh = bx1 - bx0, by1 - by0
    k = min(bw / lw, bh / lh)  # fit, keep the logo's proportions, centre in the box
    tx = bx0 + (bw - lw * k) / 2 - x0 * k
    ty = by0 + (bh - lh * k) / 2 - y0 * k
    if bg is None and box == (0, 0, 1, 1):
        # logo alone: crop to the drawing, keep its own aspect ratio
        view = f'{x0} {y0} {lw} {lh}'
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" fill="none">{logo_inner(logo)}</svg>\n'
    parts = []
    if bg and bg[0] == 'circle':
        parts.append(f'<circle cx="{S/2}" cy="{S/2}" r="{S/2}" fill="{bg[1]}"/>')
    elif bg and bg[0] == 'rounded':
        r = bg[2] * S
        parts.append(f'<rect width="{S}" height="{S}" rx="{r:.2f}" fill="{bg[1]}"/>')
    parts.append(f'<g transform="translate({tx:.3f} {ty:.3f}) scale({k:.4f})">{logo_inner(logo)}</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S:g} {S:g}" fill="none">' + ''.join(parts) + '</svg>\n'

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()
os.makedirs(OUT, exist_ok=True)
for png, (logo, bg, box) in TILES.items():
    name = png.split('/')[1] + '-' + os.path.splitext(os.path.basename(png))[0] + '.svg'
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(build(png, logo, bg, box))
    new = 'assets/vec/tiles/' + name
    n = src.count(png)
    if not n:
        raise SystemExit('not referenced: ' + png)
    src = src.replace(png, new)
open(PATH, 'w', encoding='utf-8').write(src)
print('ok', len(TILES), 'logos')
