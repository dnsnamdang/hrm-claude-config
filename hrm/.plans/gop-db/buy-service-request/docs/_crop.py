# -*- coding: utf-8 -*-
"""Cắt dải nền xám trống ở đáy ảnh chụp cả trang (fullPage) — chỉ chạy trong thư mục này."""
import os, sys
from PIL import Image
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots')

def blank(px, w, y):
    row = [px[x, y] for x in range(0, w, 7)]
    return all(abs(r - 243) < 6 and abs(g - 244) < 6 and abs(b - 246) < 6 for r, g, b in row) or \
        all(r > 238 and g > 238 and b > 238 and abs(r - b) < 6 for r, g, b in row) and False

def crop(name):
    p = os.path.join(D, name)
    im = Image.open(p).convert('RGB')
    w, h = im.size
    px = im.load()
    y = h - 1
    while y > 0 and blank(px, w, y):
        y -= 1
    # bỏ cả bóng mờ dưới footer: lùi tiếp qua các dòng gần như đồng màu
    if y < h - 200:
        im.crop((0, 0, w, min(h, y + 40))).save(p)
        print('cắt', name, h, '->', y + 40)

if __name__ == '__main__':
    for n in sorted(os.listdir(D)):
        if n.endswith('.png') and n[0].isdigit():
            crop(n)


def trim_icon(name, pad=16):
    """Cắt phần nền trống bên phải icon mục menu (khung mục rộng cả panel)."""
    from PIL import ImageChops
    p = os.path.join(D, 'icons', name)
    im = Image.open(p).convert('RGB')
    bg = Image.new('RGB', im.size, im.getpixel((im.width - 2, 2)))
    box = ImageChops.difference(im, bg).point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        im.crop((0, 0, min(im.width, box[2] + pad), im.height)).save(p)
        print('trim', name, im.width, '->', box[2] + pad)


if __name__ == '__main__':
    for n in ('menu_muc.png', 'menu_nhomcon.png'):
        trim_icon(n)
