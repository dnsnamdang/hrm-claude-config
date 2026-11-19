# -*- coding: utf-8 -*-
"""Ảnh phóng to cho PHẦN "ĐỌC BÁO CÁO" (HDSD) — 13_read_zoom (khách I, II), 13b_read_zoom (khách VII): cột STT + Khách hàng/Tuyến/Phiếu và 3 cột Cước thực tế / Thuế / Cước sau thuế,
dòng TỔNG -> nhóm III và nhóm VII, cắt từ hdsd_shots/03f_wide.png (bảng chụp khung rộng 2700px)."""
import os
from PIL import Image


def big(im):
    """Phóng lên >= 2000 px để _lib_win._fit_width chèn rộng 6,2" (ảnh < 2000 px chỉ chèn 4,5")."""
    return im.resize((2100, int(im.height * 2100 / im.width)), Image.LANCZOS) if im.width < 2000 else im
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, 'hdsd_shots')
im = Image.open(os.path.join(S, '03f_wide.png'))
k = im.width / 2000.0
def box(x0, x1, y0, y1):
    return im.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))
def row(y0, y1):
    a, b = box(0, 420, y0, y1), box(1305, 1600, y0, y1)
    out = Image.new('RGB', (a.width + 6 + b.width, a.height), 'white')
    out.paste(a, (0, 0)); out.paste(b, (a.width + 6, 0))
    return out
a = row(14, 252)
big(a).save(os.path.join(S, '13_read_zoom.png'))
hd = row(14, 46)
b = row(735, 858)
out = Image.new('RGB', (b.width, hd.height + b.height), 'white')
out.paste(hd, (0, 0)); out.paste(b, (0, hd.height))
big(out).save(os.path.join(S, '13b_read_zoom.png'))
print(a.size, out.size)
