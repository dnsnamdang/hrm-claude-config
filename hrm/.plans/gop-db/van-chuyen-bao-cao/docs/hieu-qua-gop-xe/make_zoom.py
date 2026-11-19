# -*- coding: utf-8 -*-
"""Ảnh phóng to cho PHẦN "ĐỌC BÁO CÁO" (HDSD), cắt từ hdsd_shots/03_report.png (kỳ Tháng trước, 1440px):
 13_read_money.png = STT + Công ty / Biển số xe + Số chuyến + Cước + Chi phí lái xe + Lãi gộp
 13_read_km.png    = STT + Công ty / Biển số xe + KM định mức + KM thực chạy + Chênh lệch (KM) + % Chênh lệch"""
import os
from PIL import Image


def big(im):
    """Phóng lên >= 2000 px để _lib_win._fit_width chèn rộng 6,2" (ảnh < 2000 px chỉ chèn 4,5")."""
    return im.resize((2100, int(im.height * 2100 / im.width)), Image.LANCZOS) if im.width < 2000 else im
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')
im = Image.open(os.path.join(S, '03_report.png'))
k = im.width / 2000.0
Y0, Y1 = 650, 1196


def strip(cols, name):
    parts = [im.crop((int(a * k), int(Y0 * k), int(b * k), int(Y1 * k))) for a, b in cols]
    out = Image.new('RGB', (sum(p.width for p in parts) + 4 * (len(parts) - 1), parts[0].height), (190, 190, 190))
    x = 0
    for p in parts:
        out.paste(p, (x, 0))
        x += p.width + 4
    big(out).save(os.path.join(S, name))
    print(name, out.size)


strip([(120, 743), (744, 862), (1473, 1960)], '13_read_money.png')
strip([(120, 743), (862, 1473)], '13_read_km.png')
