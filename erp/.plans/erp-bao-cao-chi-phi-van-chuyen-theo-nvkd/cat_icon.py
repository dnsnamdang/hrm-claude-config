# -*- coding: utf-8 -*-
"""Cat icon cho HDSD tu cac khung hdsd_shots/raw/{A,B,C,D}.png theo toa do phan tu (CSS px).

ERP local dang luu zoom trinh duyet 75% nen toa do CSS != pixel anh: ti le = devicePixelRatio luc chup (1.125
voi deviceScaleFactor 2 x zoom 0,75 x 0,75).
- Nut co vien/nen (btn_*, chk_*): cat dung khung phan tu, du 1px.
- Muc chi co chu (menu_*, item_*, o_*): cat sat phan chu, roi them le tren/duoi de chu chiem ~70% chieu cao
  (de khi chen cao 0,22" chu trong anh ngang co chu than bai).
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'hdsd_shots', 'raw')
ICONS = os.path.join(HERE, 'hdsd_shots', 'icons')
SCALE = 1.125  # devicePixelRatio tra ve luc chup raw/

RECTS = json.load(open(os.path.join(RAW, 'rects.json'), encoding='utf-8'))


def ink_bbox(im, thr=60):
    """Bbox phan khac mau nen (nen = mau goc tren trai)."""
    rgb = im.convert('RGB')
    bg = rgb.getpixel((0, 0))
    px = rgb.load()
    w, h = rgb.size
    xs, ys = [], []
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > thr:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def main():
    os.makedirs(ICONS, exist_ok=True)
    frames = {}
    for key, (x, y, w, h) in RECTS.items():
        f, name = key.split('|')
        im = frames.setdefault(f, Image.open(os.path.join(RAW, f + '.png')).convert('RGB'))
        s = SCALE
        box = (max(0, int(x * s)), max(0, int(y * s)), min(im.width, int((x + w) * s + 0.999)),
               min(im.height, int((y + h) * s + 0.999)))
        crop = im.crop(box)
        if name.startswith(('btn_', 'chk_')) and name != 'btn_dong_modal':
            out = crop
        else:
            bb = ink_bbox(crop)
            if bb:
                crop = crop.crop(bb)
            ink_h = crop.height
            H = max(int(ink_h * 1.4), ink_h + 6)
            pad_x = max(3, int(ink_h * 0.2))
            out = Image.new('RGB', (crop.width + 2 * pad_x, H), im.getpixel((box[0], box[1])) if name.startswith('menu_') else 'white')
            out.paste(crop, (pad_x, (H - ink_h) // 2))
        out.save(os.path.join(ICONS, name + '.png'))
        print(name, out.size)


if __name__ == '__main__':
    main()
