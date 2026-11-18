# -*- coding: utf-8 -*-
"""Cắt phần nền trống phía dưới các ảnh chụp cả trang (fullPage) của 2 màn thừa thiếu. Chạy: python trim_shots.py <thư mục hdsd_shots>"""
import os
import sys
from PIL import Image, ImageStat

d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith('.png'):
        continue
    p = os.path.join(d, f)
    im = Image.open(p).convert('RGB')
    w, h = im.size
    if h <= 1900:
        continue
    g = im.convert('L')
    last = h
    for y in range(h - 1, 0, -4):
        row = g.crop((int(w * 0.1), y, w, y + 1))
        if ImageStat.Stat(row).stddev[0] > 6:
            last = y
            break
    if last < h - 40:
        im.crop((0, 0, w, min(h, last + 30))).save(p)
        print('trim', f, h, '->', last + 30)
