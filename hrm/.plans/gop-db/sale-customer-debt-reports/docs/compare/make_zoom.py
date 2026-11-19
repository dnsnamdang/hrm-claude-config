# -*- coding: utf-8 -*-
"""Ghép ảnh phóng to cho PHẦN ĐỌC BÁO CÁO (HDSD): cột STT + 8 cột số (2 mảnh chụp thật từ capture.js bước zoom)."""
import os
from PIL import Image, ImageDraw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')
a = Image.open(os.path.join(D, '_zoom_a.png')).convert('RGB')
b = Image.open(os.path.join(D, '_zoom_b.png')).convert('RGB')
gap = 24
W = max(2000, a.width + gap + b.width)
im = Image.new('RGB', (W, max(a.height, b.height)), 'white')
im.paste(a, (0, 0))
x = a.width + gap
d = ImageDraw.Draw(im)
for k in range(0, im.height, 16):  # đường đứt: báo phần cột ở giữa đã lược
    d.line([(a.width + gap // 2, k), (a.width + gap // 2, k + 8)], fill=(150, 150, 150), width=3)
im.paste(b, (x, 0))
im.save(os.path.join(D, '12_read_zoom.png'))
print(im.size)
