#!/usr/bin/env python3
"""Render header.gif (animated waves behind the header artwork) and header.png (first frame, for clients that
don't animate GIFs, like desktop Outlook).

Needs: rsvg-convert (brew install librsvg) and Pillow (pip install pillow).
header.svg is the artwork. Everything before its first <g transform=...> is the background; the rest sits on top
of the waves.   Usage: python3 build-header-gif.py [width]   (default 1200)
"""
import io, math, re, subprocess, sys
from PIL import Image

W, H = 1200, 400
OUT_W = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
FRAMES, DELAY_MS = 36, 100            # a 3.6 s seamless loop

# One wave recipe, taken from the slides' wave engine (same layers, same colours).
P = dict(base=.70, tilt=.10, amp=1.0, f1=.9, f2=1.8, a2=.4, f3=5, a3=.15, p=1.0, gap=.06, hue=.3)
LAYERS, BOOST, STEP = 5, 1.9, 8

svg = open('header.svg').read()
cut = svg.index('<g transform=')
back, front = svg[:cut], svg[cut:]

def waves(tau):
    out = ['<defs><linearGradient id="hs" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="%d" y2="0">'
           '<stop offset="0" stop-color="#2dd4bf" stop-opacity=".55"/><stop offset="1" stop-color="#8b5cf6" stop-opacity=".55"/>'
           '</linearGradient></defs>' % W]
    for l in range(LAYERS):
        f = l / (LAYERS - 1)
        A = H * .04 * P['amp'] * (1 + .28 * l) * BOOST
        base_y = H * (P['base'] + l * P['gap'])
        k1 = 2 * math.pi * P['f1'] / (W * (.8 + .12 * l))
        k2 = 2 * math.pi * P['f2'] / (W * (.38 + .05 * l))
        k3 = 2 * math.pi * P['f3'] / (W * (.25 + .04 * l))
        ph = l * 1.7 + P['hue'] * 2 * math.pi
        a1, a2, a3 = 2 * math.pi * tau, -2 * math.pi * tau, 2 * math.pi * 2 * tau   # whole cycles per loop
        pts = []
        for x in range(0, W + STEP + 1, STEP):
            s1 = math.sin(x * k1 + a1 + ph)
            v1 = math.copysign(abs(s1) ** P['p'], s1)
            y = base_y + P['tilt'] * H * (x / W - .5) + A * (v1 + P['a2'] * math.sin(x * k2 + a2 + ph * 1.9)
                                                             + P['a3'] * math.sin(x * k3 + a3 + ph * 2.7))
            pts.append((x, y))
        line = 'M' + ' L'.join('%d,%.1f' % p for p in pts)
        mix = (math.sin(l * 1.3 + P['hue'] * 2 * math.pi) + 1) / 2
        r, g, b = (round(45 + (139 - 45) * (1 - mix)), round(212 + (92 - 212) * (1 - mix)), round(191 + (246 - 191) * (1 - mix)))
        gid = 'wf%d' % l
        out.append('<defs><linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="0" y1="%.1f" x2="0" y2="%d">'
                   '<stop offset="0" stop-color="rgb(%d,%d,%d)" stop-opacity=".30"/>'
                   '<stop offset="1" stop-color="rgb(%d,%d,%d)" stop-opacity="0"/></linearGradient></defs>'
                   % (gid, base_y - A * 1.5, H, r, g, b, r, g, b))
        out.append('<path d="%s L%d,%d L0,%d Z" fill="url(#%s)"/>' % (line, W + STEP, H, H, gid))
        out.append('<path d="%s" fill="none" stroke="url(#hs)" stroke-width="1.6" stroke-opacity="%.2f"/>' % (line, .45 + .15 * (1 - f)))
    return ''.join(out)

frames = []
for i in range(FRAMES):
    doc = back + waves(i / FRAMES) + front + '</svg>' if not front.rstrip().endswith('</svg>') else back + waves(i / FRAMES) + front
    png = subprocess.run(['rsvg-convert', '-w', str(OUT_W)], input=doc.encode(), capture_output=True, check=True).stdout
    frames.append(Image.open(io.BytesIO(png)).convert('RGB'))

frames[0].save('header.png')
pal = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
gif = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
gif[0].save('header.gif', save_all=True, append_images=gif[1:], duration=DELAY_MS, loop=0, optimize=True, disposal=1)
print('header.gif', OUT_W, 'x', OUT_W * H // W, FRAMES, 'frames')
