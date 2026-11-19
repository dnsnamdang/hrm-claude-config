#!/usr/bin/env python3
"""Dựng video từ rec_L.mov + rec_R.mov + timeline.json (record.py) → huong-dan-meeting-app.mp4 (1920×1080)."""
import json, os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
T = json.load(open(os.path.join(HERE, os.environ.get('TL', 'timeline.json'))))
W, H = 1920, 1080
PH_H = 900
PH_W = round(1206 * PH_H / 2622)          # 414
K = PH_H / 874                            # điểm → px khung dựng
PY = 52
PX = {'L': 470, 'R': 1036}
R_IN = 46                                 # bo góc màn
BEZ = 9
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def font(sz, bold=False):
    try:
        return ImageFont.truetype(FB if bold else FONT, sz)
    except Exception:
        return ImageFont.truetype(FONT, sz)


# ── lớp nền có lỗ cho 2 màn hình + viền máy + nhãn vai trò ──────────────────
bg = Image.new('RGBA', (W, H))
d = ImageDraw.Draw(bg)
for y in range(H):
    a = y / H
    d.line([(0, y), (W, y)], fill=(int(14 + 10 * a), int(38 + 30 * a), int(58 + 26 * a), 255))
ROLE_R = os.environ.get('ROLE_R', 'NGƯỜI THAM GIA')
for side, title, sub in (('L', 'CHỦ TRÌ', 'DNS Admin'), ('R', ROLE_R, 'Đào Thị Thúy')):
    x0 = PX[side]
    d.rounded_rectangle([x0 - BEZ, PY - BEZ, x0 + PH_W + BEZ, PY + PH_H + BEZ], radius=R_IN + BEZ, fill=(10, 14, 20, 255))
    d.rounded_rectangle([x0, PY, x0 + PH_W, PY + PH_H], radius=R_IN, fill=(0, 0, 0, 0))
    lab = f'{title} · {sub}'
    f = font(24, True)
    tw = d.textlength(lab, font=f)
    cx = x0 + PH_W / 2
    d.rounded_rectangle([cx - tw / 2 - 16, 8, cx + tw / 2 + 16, 44], radius=18,
                        fill=(26, 188, 156, 235) if side == 'L' else (59, 130, 246, 235))
    d.text((cx - tw / 2, 12), lab, font=f, fill='white')
# lỗ trong suốt: vẽ lại vùng màn hình bằng alpha 0
mask = Image.new('L', (W, H), 255)
md = ImageDraw.Draw(mask)
for side in ('L', 'R'):
    x0 = PX[side]
    md.rounded_rectangle([x0, PY, x0 + PH_W, PY + PH_H], radius=R_IN, fill=0)
bg.putalpha(mask)
bg.save(os.path.join(OUT, 'fg.png'))

# ── phụ đề + tên chương ────────────────────────────────────────────────────
def caption_png(i, s):
    f = font(30)
    lines = textwrap.wrap(s, 78)
    lh = 40
    tw = max(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(l, font=f) for l in lines)
    im = Image.new('RGBA', (int(tw) + 48, lh * len(lines) + 22), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=14, fill=(0, 0, 0, 175))
    for k, l in enumerate(lines):
        lw = dd.textlength(l, font=f)
        dd.text(((im.width - lw) / 2, 10 + k * lh), l, font=f, fill='white')
    p = os.path.join(OUT, f'cap{i:02d}.png')
    im.save(p)
    return p, im.width, im.height


def chapter_png(name, k):
    f = font(30, True)
    tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(name, font=f)
    im = Image.new('RGBA', (int(tw) + 56, 56), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.rounded_rectangle([0, 0, im.width - 1, 55], radius=12, fill=(37, 99, 235, 230))
    dd.text((28, 9), name, font=f, fill='white')
    p = os.path.join(OUT, f'chap{k}.png')
    im.save(p)
    return p


dot = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
ImageDraw.Draw(dot).ellipse([4, 4, 56, 56], fill=(239, 68, 68, 150), outline=(255, 255, 255, 230), width=4)
dot.save(os.path.join(OUT, 'dot.png'))


def mark_png(k, w, h):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([2, 2, w - 3, h - 3], radius=14, outline=(250, 204, 21, 255), width=5)
    p = os.path.join(OUT, f'mark{k}.png')
    im.save(p)
    return p


steps = T['steps']
end = T['end']
inputs, ov = [], []   # ov: (input_idx, x, y, t0, t1)
# chương
chaps = []
for s in steps:
    if not chaps or chaps[-1][0] != s['ch']:
        chaps.append([s['ch'], s['start'], s['end']])
    chaps[-1][2] = s['end']
for k, (name, a, b) in enumerate(chaps):
    inputs.append(chapter_png(name, k)); ov.append((len(inputs) - 1, 40, 60, a, b))
# phụ đề
for s in steps:
    p, w, h = caption_png(s['i'], s['say'])
    inputs.append(p); ov.append((len(inputs) - 1, (W - w) // 2, H - h - 10, s['start'], s['end']))
# khung vàng
mk = 0
for s in steps:
    for m in s['mark']:
        side, x, y, w, h = m[:5]
        off = m[5] if len(m) > 5 else 0.3
        pw, ph = round(w * K), round(h * K)
        inputs.append(mark_png(mk, pw, ph)); mk += 1
        ov.append((len(inputs) - 1, PX[side] + round(x * K), PY + round(y * K), s['start'] + off, min(s['end'], s['start'] + off + 4.2)))
# chấm chạm
inputs.append(os.path.join(OUT, 'dot.png')); di = len(inputs) - 1
for t in T['taps']:
    ov.append((di, PX[t['dev']] + round(t['x'] * K) - 30, PY + round(t['y'] * K) - 30, t['t'], t['t'] + 0.6))

args = ['ffmpeg', '-y', '-loglevel', 'error']
for side in ('L', 'R'):
    args += ['-ss', str(T['offs'][side]), '-i', os.path.join(HERE, f'rec_{side}.mov')]
args += ['-loop', '1', '-i', os.path.join(OUT, 'fg.png')]
base = 3
for p in inputs:
    args += ['-loop', '1', '-i', p]
abase = base + len(inputs)
for s in steps:
    args += ['-i', s['audio']]

fc = [f'color=c=black:s={W}x{H}:r=30:d={end:.3f}[c0]']
for k, side in enumerate(('L', 'R')):
    fc.append(f'[{k}:v]fps=30,scale={PH_W}:{PH_H},setpts=PTS-STARTPTS[p{side}]')
fc.append(f"[c0][pL]overlay={PX['L']}:{PY}:eof_action=repeat[c1]")
fc.append(f"[c1][pR]overlay={PX['R']}:{PY}:eof_action=repeat[c2]")
fc.append('[c2][2:v]overlay=0:0:shortest=1[c3]')
cur = 'c3'
for n, (idx, x, y, a, b) in enumerate(ov):
    nxt = f'o{n}'
    fc.append(f"[{cur}][{base + idx}:v]overlay={x}:{y}:enable='between(t,{a:.2f},{b:.2f})':shortest=1[{nxt}]")
    cur = nxt
labels = []
for k, s in enumerate(steps):
    ms = int(round((s['start'] + 0.15) * 1000))
    fc.append(f'[{abase + k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]')
    labels.append(f'[a{k}]')
fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,volume=1.15,alimiter=limit=0.89:level=false,apad,atrim=0:{end:.3f}[aout]')
script = os.path.join(OUT, 'filter.txt')
open(script, 'w').write(';\n'.join(fc))
OUTN = os.environ.get('OUT', 'huong-dan-meeting-app')
final = os.path.join(HERE, OUTN + '.mp4')
args += ['-/filter_complex', script, '-map', f'[{cur}]', '-map', '[aout]', '-t', f'{end:.3f}',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k', '-movflags', '+faststart', final]
subprocess.run(args, check=True)
light = os.path.join(HERE, OUTN + '-ban-nhe.mp4')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', final, '-c:v', 'libx264', '-preset', 'slow', '-crf', '27',
                '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', light], check=True)
for f in (final, light):
    print(os.path.basename(f), subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', f],
                                               capture_output=True, text=True).stdout.strip())
