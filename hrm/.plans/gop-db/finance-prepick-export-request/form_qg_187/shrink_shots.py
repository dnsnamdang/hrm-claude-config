# -*- coding: utf-8 -*-
"""Ảnh chụp ở deviceScaleFactor 2 (2880 px) làm file Word ~10 MB -> thu về rộng 1600 px (đủ nét khi chèn 6,2").
Dùng: python shrink_shots.py <thư mục hdsd_shots>   (không đụng thư mục icons/)"""
import os, sys
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    p = os.path.join(d, f)
    if not f.endswith('.png') or not os.path.isfile(p):
        continue
    im = Image.open(p)
    if im.width > 1600:
        im.convert('RGB').resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(p, optimize=True)
        print('thu nhỏ', f)
