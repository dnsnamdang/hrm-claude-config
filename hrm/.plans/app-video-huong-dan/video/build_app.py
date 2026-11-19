#!/usr/bin/env python3
"""Dựng video 1 máy ảo từ timeline_<name>.json (vc.run) → <OUT>.mp4 1920×1080 + bản nhẹ.

Dựng THEO TỪNG BƯỚC rồi nối (bản cũ ghép ~350 lớp lên cả 17' trong 1 lệnh ffmpeg ⇒ chạy 1 luồng, treo 6 tiếng, 09/11):
- mỗi bước = 1 đoạn: hình máy (bỏ các đoạn `cuts` đang tải) + 1 ảnh nền tĩnh (viền máy + mục lục chương + phụ đề)
  + khung vàng + chấm chạm của bước đó + clip ngoài (nếu có) + lời đọc; các đoạn dựng song song.
- nối bằng concat (copy), rồi xuất bản nhẹ crf 27.
Chạy: NAME=mytodo OUT=huong-dan-viec-cua-toi python3 build_app.py   (JOBS=6 số đoạn dựng song song)
"""
import json, os, subprocess, textwrap
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get('VWORK', os.path.expanduser('~/.cache/tpe-video-work'))
NAME = os.environ.get('NAME', 'mytodo')
OUTN = os.environ.get('OUT', 'huong-dan-viec-cua-toi')
JOBS = int(os.environ.get('JOBS', '6'))
T = json.load(open(os.path.join(WORK, f'timeline_{NAME}.json')))
OV = os.path.join(WORK, f'ov_{NAME}')
SEG = os.path.join(WORK, f'seg_{NAME}')
os.makedirs(OV, exist_ok=True)
os.makedirs(SEG, exist_ok=True)
W, H = 1920, 1080
PH_H = 900
PH_W = round(1206 * PH_H / 2622)          # 414
K = PH_H / 874
PX, PY = (W - PH_W) // 2, 40
R_IN, BEZ = 46, 9
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
FPS = 30


def font(sz, bold=False):
    try:
        return ImageFont.truetype(FB if bold else FONT, sz)
    except Exception:
        return ImageFont.truetype(FONT, sz)


cuts = sorted((a, b) for a, b in T['cuts'] if b > a)


def mt(t):
    d = 0.0
    for a, b in cuts:
        if t >= b:
            d += b - a
        elif t > a:
            d += t - a
    return t - d


steps = T['steps']
for k, s in enumerate(steps):
    s['t0'] = s['start']
    s['t1'] = steps[k + 1]['start'] if k + 1 < len(steps) else T['end']
    s['dur'] = round(mt(s['t1']) - mt(s['t0']), 3)

# ── bản quay gốc → 30 khung/giây ĐỀU, đã thu về khung máy 414×900 ───────────
# simctl recordVideo chỉ ghi khung khi màn ĐỔI ⇒ khúc màn đứng yên bị cắt ra không có khung nào ⇒ ra màn ĐEN (09/11).
CFR = os.path.join(WORK, f'cfr_{NAME}.mp4')
if not os.path.exists(CFR) or os.path.getmtime(CFR) < os.path.getmtime(T['rec']):
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', T['rec'], '-vf', f'fps={FPS},scale={PH_W}:{PH_H}',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-g', '30', '-an', CFR], check=True, stdin=subprocess.DEVNULL)
    print('Đã chuẩn hoá bản quay', flush=True)

# ── ảnh nền tĩnh cho từng bước ─────────────────────────────────────────────
base = Image.new('RGBA', (W, H))
d = ImageDraw.Draw(base)
for y in range(H):
    a = y / H
    d.line([(0, y), (W, y)], fill=(int(14 + 10 * a), int(38 + 30 * a), int(58 + 26 * a), 255))
d.rounded_rectangle([PX - BEZ, PY - BEZ, PX + PH_W + BEZ, PY + PH_H + BEZ], radius=R_IN + BEZ, fill=(10, 14, 20, 255))
d.text((PX + PH_W + 60, 60), 'ERP TPE · ỨNG DỤNG DI ĐỘNG', font=font(22, True), fill=(148, 197, 255, 255))
d.text((PX + PH_W + 60, 92), os.environ.get('TITLE', 'VIỆC CỦA TÔI · NHẮC VIỆC CÁ NHÂN'), font=font(26, True), fill='white')
HOLE = Image.new('L', (W, H), 255)
ImageDraw.Draw(HOLE).rounded_rectangle([PX, PY, PX + PH_W, PY + PH_H], radius=R_IN, fill=0)

chaps = []
for s in steps:
    if s['ch'] not in chaps:
        chaps.append(s['ch'])


def step_png(i, s):
    im = base.copy()
    dd = ImageDraw.Draw(im)
    y = 70
    for k, c in enumerate(chaps):
        on = c == s['ch']
        lab = f'{k + 1:>2}. {c}'
        f_ = font(24, on)
        if on:
            tw = dd.textlength(lab, font=f_)
            dd.rounded_rectangle([40, y - 6, 40 + tw + 28, y + 34], radius=10, fill=(37, 99, 235, 235))
        dd.text((54, y), lab, font=f_, fill='white' if on else (190, 205, 220, 255))
        y += 48
    fs = font(28)
    lines = textwrap.wrap(s['say'], 92)[:3]
    lh = 36
    tw = max(dd.textlength(l, font=fs) for l in lines)
    bw, bh = int(tw) + 48, lh * len(lines) + 20
    x0, y0 = (W - bw) // 2, H - bh - 8
    dd.rounded_rectangle([x0, y0, x0 + bw - 1, y0 + bh - 1], radius=14, fill=(0, 0, 0, 200))
    for k, l in enumerate(lines):
        dd.text(((W - dd.textlength(l, font=fs)) / 2, y0 + 8 + k * lh), l, font=fs, fill='white')
    # khoét lỗ màn hình (phụ đề đè lên mép dưới máy vẫn giữ)
    alpha = im.getchannel('A')
    sub = Image.new('L', (W, H), 0)
    ImageDraw.Draw(sub).rounded_rectangle([x0, y0, x0 + bw - 1, y0 + bh - 1], radius=14, fill=255)
    im.putalpha(Image.composite(alpha, Image.new('L', (W, H), 0), Image.composite(Image.new('L', (W, H), 255), HOLE, sub)))
    p = os.path.join(OV, f'bg{i:03d}.png')
    im.save(p)
    return p


dot = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
ImageDraw.Draw(dot).ellipse([4, 4, 56, 56], fill=(239, 68, 68, 150), outline=(255, 255, 255, 230), width=4)
DOT = os.path.join(OV, 'dot.png')
dot.save(DOT)


def mark_png(i, k, w_, h_):
    im = Image.new('RGBA', (w_, h_), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([2, 2, w_ - 3, h_ - 3], radius=14, outline=(250, 204, 21, 255), width=5)
    p = os.path.join(OV, f'mk{i:03d}_{k}.png')
    im.save(p)
    return p


def build_step(s):
    i = s['i']
    out = os.path.join(SEG, f'{i:03d}.mp4')
    dur = s['dur']
    if dur <= 0.05:
        return None
    keep, t = [], s['t0']
    for a, b in cuts:
        if b <= s['t0'] or a >= s['t1']:
            continue
        if a > t:
            keep.append((t, a))
        t = max(t, b)
    if t < s['t1']:
        keep.append((t, s['t1']))
    rel = lambda x: round(mt(x) - mt(s['t0']), 3)
    if os.path.exists(out) and os.path.getsize(out) > 1000 and not os.environ.get('FORCE'):
        return out          # đã dựng ở lượt trước (FORCE=1 để dựng lại)
    args = ['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-ss', f"{s['t0']:.3f}", '-t', f"{s['t1'] - s['t0'] + 0.3:.3f}", '-i', CFR,
            '-loop', '1', '-i', step_png(i, s), '-i', s['audio']]
    n_in = 3
    g, parts = [], []
    for k, (a, b) in enumerate(keep):
        g.append(f'[0:v]trim=start={a - s["t0"]:.3f}:end={b - s["t0"]:.3f},setpts=PTS-STARTPTS[k{k}]')
        parts.append(f'[k{k}]')
    g.append(''.join(parts) + f'concat=n={len(parts)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=3[ph]')
    g.append(f'color=c=black:s={W}x{H}:r={FPS}:d={dur:.3f}[c0]')
    g.append(f'[c0][ph]overlay={PX}:{PY}:eof_action=repeat[c1]')
    cur = 'c1'
    clip_in = None
    if s.get('clip'):
        args += ['-i', os.path.join(HERE, s['clip'])]
        clip_in = n_in; n_in += 1
        g.append(f'[{clip_in}:v]fps={FPS},scale={PH_W}:{PH_H},tpad=stop_mode=clone:stop_duration=30[cl]')
        g.append(f'[{cur}][cl]overlay={PX}:{PY}:eof_action=repeat[c2]')
        cur = 'c2'
    g.append(f'[{cur}][1:v]overlay=0:0:shortest=1[c3]')
    cur = 'c3'
    for k, m in enumerate(s['mark']):
        x, y, w_, h_ = m[:4]
        a = max(0.0, min(dur, m[4] if len(m) > 4 else 0.3))
        args += ['-loop', '1', '-i', mark_png(i, k, max(8, round(w_ * K)), max(8, round(h_ * K)))]
        g.append(f"[{cur}][{n_in}:v]overlay={PX + round(x * K)}:{PY + round(y * K)}:enable='between(t,{a:.2f},{min(dur, a + 4.2):.2f})':shortest=1[m{k}]")
        cur = f'm{k}'; n_in += 1
    for k, t_ in enumerate(x for x in T['taps'] if s['t0'] <= x['t'] < s['t1']):
        a = rel(t_['t'])
        args += ['-loop', '1', '-i', DOT]
        g.append(f"[{cur}][{n_in}:v]overlay={PX + round(t_['x'] * K) - 30}:{PY + round(t_['y'] * K) - 30}:enable='between(t,{a:.2f},{a + 0.6:.2f})':shortest=1[d{k}]")
        cur = f'd{k}'; n_in += 1
    g.append('[2:a]aresample=48000,aformat=channel_layouts=stereo,adelay=150|150[na]')
    src = '[na]'
    if clip_in is not None:   # tiếng của clip (tút gọi) nhỏ dưới lời đọc
        g.append(f'[{clip_in}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.35[ca]')
        g.append('[na][ca]amix=inputs=2:normalize=0[mx]')
        src = '[mx]'
    g.append(f'{src}volume=1.15,alimiter=limit=0.89:level=false,apad,atrim=0:{dur:.3f}[aout]')
    script = os.path.join(SEG, f'{i:03d}.txt')
    open(script, 'w').write(';\n'.join(g))
    args += ['-/filter_complex', script, '-map', f'[{cur}]', '-map', '[aout]', '-t', f'{dur:.3f}', '-r', str(FPS),
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-ar', '48000', '-ac', '2', '-b:a', '192k', out]
    r = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise SystemExit(f'Bước {i} lỗi dựng: {r.stderr[-800:]}')
    return out


only = os.environ.get('ONLY')          # vd ONLY=0-5 để dựng thử vài bước
todo = steps
if only:
    a, b = map(int, only.split('-'))
    todo = [s for s in steps if a <= s['i'] <= b]
with ThreadPoolExecutor(JOBS) as ex:
    outs = [o for o in ex.map(build_step, todo) if o]
print('Đã dựng', len(outs), 'đoạn', flush=True)
lst = os.path.join(SEG, 'list.txt')
open(lst, 'w').write(''.join(f"file '{o}'\n" for o in outs))
final = os.path.join(HERE, OUTN + '.mp4')
subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                '-movflags', '+faststart', final], check=True)
if not only:
    light = os.path.join(HERE, OUTN + '-ban-nhe.mp4')
    subprocess.run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', final, '-c:v', 'libx264', '-preset', 'medium', '-crf', '27',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', light], check=True)
    finals = (final, light)
else:
    finals = (final,)
for f_ in finals:
    print(os.path.basename(f_), subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', f_],
                                                capture_output=True, text=True).stdout.strip(), flush=True)
