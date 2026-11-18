# -*- coding: utf-8 -*-
"""Ghép ảnh phóng to cho PHẦN ĐỌC BÁO CÁO (HDSD): cắt cột trái (STT + tên) và cột số bên phải từ ảnh thật 05_read.png
(khuôn compare/make_zoom.py). Dùng: python make_zoom.py <thư mục màn> <tỉ lệ trái> <tỉ lệ phải bắt đầu>"""
import os
import sys
from PIL import Image, ImageDraw
D = os.path.join(sys.argv[1], 'hdsd_shots')
lw, rs = float(sys.argv[2]), float(sys.argv[3])
im0 = Image.open(os.path.join(D, '05_read.png')).convert('RGB')
W0, H0 = im0.size
a = im0.crop((0, 0, int(W0 * lw), H0))
b = im0.crop((int(W0 * rs), 0, W0, H0))
gap = 24
im = Image.new('RGB', (a.width + gap + b.width, H0), 'white')
im.paste(a, (0, 0))
d = ImageDraw.Draw(im)
for k in range(0, H0, 16):  # đường đứt: phần cột ở giữa đã lược
    d.line([(a.width + gap // 2, k), (a.width + gap // 2, k + 8)], fill=(150, 150, 150), width=3)
im.paste(b, (a.width + gap, 0))
im.save(os.path.join(D, '05c_read_zoom.png'))
print(im.size)
