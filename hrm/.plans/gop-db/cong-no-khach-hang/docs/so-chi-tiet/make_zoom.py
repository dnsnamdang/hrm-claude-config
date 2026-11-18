# -*- coding: utf-8 -*-
"""Ảnh phóng to cho PHẦN ĐỌC BÁO CÁO (HDSD): ghép cột STT + Số chứng từ + nhãn dòng tổng + Phát sinh nợ/có + Tài khoản đối ứng
từ ảnh chụp thật 12_read_zoom_full.png (capture.js bước zoom) — bảng 11 cột chèn 6" thì chữ số quá nhỏ."""
import os
from PIL import Image, ImageDraw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')
src = os.path.join(D, '12_read_zoom_full.png')
if not os.path.exists(src):
    os.rename(os.path.join(D, '12_read_zoom.png'), src)
im = Image.open(src).convert('RGB')
parts = [(0, 111), (981, 1281), (2250, 3082)]
gap = 24
W = sum(b - a for a, b in parts) + gap * (len(parts) - 1)
out = Image.new('RGB', (W, im.height), 'white')
d = ImageDraw.Draw(out)
x = 0
for i, (a, b) in enumerate(parts):
    out.paste(im.crop((a, 0, b, im.height)), (x, 0))
    x += b - a
    if i < len(parts) - 1:
        for k in range(0, im.height, 16):
            d.line([(x + gap // 2, k), (x + gap // 2, k + 8)], fill=(150, 150, 150), width=3)
        x += gap
out.save(os.path.join(D, '12_read_zoom.png'))
print(out.size)
