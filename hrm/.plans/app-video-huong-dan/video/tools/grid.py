#!/usr/bin/env python3
"""Lưới khung hình kiểm video: mỗi bước 1 khung (OFF giây trước khi sang bước sau). python3 tools/grid.py [OFF]"""
import json, os, subprocess, sys
W = os.path.expanduser('~/.cache/tpe-video-work')
V = sys.argv[2] if len(sys.argv) > 2 else 'huong-dan-viec-cua-toi.mp4'
OFF = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4
t = json.load(open(f'{W}/timeline_mytodo.json'))
cuts = sorted((a, b) for a, b in t['cuts'] if b > a)
mt = lambda x: x - sum((b - a) if x >= b else max(0, x - a) for a, b in cuts)
S = t['steps']
os.makedirs(f'{W}/chk', exist_ok=True)
SEG = f'{W}/seg_mytodo'
for k, s in enumerate(S):
    f = f'{SEG}/{k:03d}.mp4'
    if not os.path.exists(f):
        continue
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                             capture_output=True, text=True).stdout.strip() or 0)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{max(0.05, d - OFF):.2f}', '-i', f, '-frames:v', '1',
                    '-vf', 'crop=414:900:753:40,scale=207:450', f'{W}/chk/{k:03d}.png'])
for g in range(0, len(S), 24):
    ins = [f'{W}/chk/{k:03d}.png' for k in range(g, min(g + 24, len(S))) if os.path.exists(f'{W}/chk/{k:03d}.png')]
    args = ['ffmpeg', '-nostdin', '-v', 'error', '-y']
    for p in ins:
        args += ['-i', p]
    lay = '|'.join(f'{(i % 12) * 207}_{(i // 12) * 450}' for i in range(len(ins)))
    args += ['-filter_complex', ''.join(f'[{i}:v]' for i in range(len(ins))) + f'xstack=inputs={len(ins)}:layout={lay}:fill=black',
             '-frames:v', '1', f'{W}/chk/grid{g:03d}.png']
    subprocess.run(args)
print('ok')
