# -*- coding: utf-8 -*-
"""Ảnh phóng to cho PHẦN ĐỌC BÁO CÁO (HDSD): cột STT..Số chứng từ + cột Ghi chú (nhãn 3 dòng tổng) + 2 cột Phát sinh nợ / Phát sinh có, cắt từ 04b_employee_table.png."""
import os
from PIL import Image, ImageDraw
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')
src = Image.open(os.path.join(D, '04b_employee_table.png')).convert('RGB')
H = 1052
a = src.crop((52, 112, 1111, H))
b = src.crop((1873, 112, 2964, H))
gap = 24
im = Image.new('RGB', (a.width + gap + b.width, a.height), 'white')
im.paste(a, (0, 0))
d = ImageDraw.Draw(im)
for k in range(0, im.height, 16):
    d.line([(a.width + gap // 2, k), (a.width + gap // 2, k + 8)], fill=(150, 150, 150), width=3)
im.paste(b, (a.width + gap, 0))
im.save(os.path.join(D, '12_read_zoom.png'))
print(im.size)
