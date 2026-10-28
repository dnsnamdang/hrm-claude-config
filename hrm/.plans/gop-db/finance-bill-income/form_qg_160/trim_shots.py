# -*- coding: utf-8 -*-
"""Cắt dải nền trống ở đáy ảnh chụp cả trang (fullPage) — trang có min-height cao hơn nội dung.
Chạy: python trim_shots.py 10_create 12_edit ...   (tên ảnh trong hdsd_shots, không đuôi)"""
import os, sys
from PIL import Image, ImageChops
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')
for n in sys.argv[1:]:
    p = os.path.join(D, n + '.png')
    im = Image.open(p).convert('RGB')
    bg = im.getpixel((im.width // 2, im.height - 1))
    diff = ImageChops.difference(im, Image.new('RGB', im.size, bg)).convert('L').point(lambda v: 255 if v > 8 else 0)
    box = diff.getbbox()
    if box and box[3] < im.height - 4:
        im.crop((0, 0, im.width, min(im.height, box[3] + 12))).save(p)
        print('trim', n, im.height, '->', box[3] + 12)
