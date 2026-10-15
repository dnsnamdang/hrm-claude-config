# -*- coding: utf-8 -*-
"""Cat anh + icon cho HDSD 2 bao cao cong no (Doi chieu 1 KH, Tong hop theo NV) tu hdsd_shots/raw/.

Chup ERP local 12/10/2026 (zoom profile 75% + deviceScaleFactor 2): toa do CSS x 1.125 = pixel anh.
- Anh minh hoa: cat theo pixel (do tren anh raw).
- Icon nut (btn_*): cat dung khung phan tu. Icon chu (o_*, menu_*, item_*): cat sat chu + them le.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'hdsd_shots', 'raw')
SHOTS = os.path.join(HERE, 'hdsd_shots')
ICONS = os.path.join(SHOTS, 'icons')
S = 1.125

# anh minh hoa: ten -> (file raw, box pixel)
ANH = {
    'dc_01_list': ('dc_raw_list', (0, 64, 1790, 1112)),
    'dc_02_popup': ('dc_raw_popup', (262, 12, 1540, 345)),
    'dc_03_err': ('dc_raw_err', (0, 0, 1790, 560)),
    'nv_01_list': ('nv_raw_list', (0, 64, 1770, 1125)),
    'nv_02_right': ('nv_raw_right', (0, 64, 1770, 1125)),
    'menu_cong_no': ('raw_menu', (0, 0, 672, 516)),
}

# icon: ten -> (file raw, rect CSS [x, y, w, h])
ICON = {
    'o_tungay': ('dc_raw_list', [30, 110.8, 75.5, 19.5]),
    'o_denngay': ('dc_raw_list', [427.5, 110.8, 82.5, 19.5]),
    'o_khachhang': ('dc_raw_list', [825, 110.8, 97, 19.5]),
    'o_sohopdong': ('dc_raw_list', [1222.5, 110.8, 84.2, 19.5]),
    'o_congty': ('dc_raw_list', [30, 229.3, 54.7, 19.5]),
    'o_phongban': ('dc_raw_list', [427.5, 229.3, 72.5, 19.5]),
    'o_bophan': ('dc_raw_list', [825, 229.3, 57.7, 19.5]),
    'o_nhanvien': ('dc_raw_list', [1222.5, 229.3, 68.3, 19.5]),
    'btn_loc': ('dc_raw_list', [20, 295, 58.6, 30.5]),
    'btn_lammoi': ('dc_raw_list', [81.8, 295, 34.6, 30.5]),
    'btn_xuatexcel': ('dc_raw_list', [119.7, 295, 99.8, 30.5]),
    'btn_in': ('dc_raw_list', [222.7, 295, 50.2, 30.5]),
    'btn_chitiet': ('dc_raw_popup', [1209.5, 251.8, 66.8, 30.5]),
    'btn_huy': ('dc_raw_popup', [1284.3, 251.8, 59.8, 30.5]),
    'o_soducuoiky': ('nv_raw_list', [30, 166.5, 88.5, 19.5]),
    'o_ngaynghiemthu': ('nv_raw_list', [422.4, 166.5, 109.1, 19.5]),
    'btn_xuatexcel_mauin': ('nv_raw_list', [1007.5, 232.2, 143.4, 30.5]),
    'menu_bccongno': ('raw_menu', [0, 290, 180, 40]),
    'item_doichieu': ('raw_menu', [215, 87.4, 250.5, 16.9]),
    'item_theonv': ('raw_menu', [215, 113.4, 350.6, 16.9]),
}


def ink_bbox(im, thr=60, bg=None):
    rgb = im.convert('RGB')
    bg = bg or rgb.getpixel((0, 0))
    px = rgb.load()
    xs, ys = [], []
    for y in range(rgb.height):
        for x in range(rgb.width):
            r, g, b = px[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > thr:
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def main():
    os.makedirs(ICONS, exist_ok=True)
    cache = {}

    def raw(f):
        return cache.setdefault(f, Image.open(os.path.join(RAW, f + '.png')).convert('RGB'))

    for name, (f, box) in ANH.items():
        raw(f).crop(box).save(os.path.join(SHOTS, name + '.png'))
        print('anh', name)
    for name, (f, (x, y, w, h)) in ICON.items():
        im = raw(f)
        box = (max(0, int(x * S)), max(0, int(y * S)), min(im.width, int((x + w) * S + 0.999)),
               min(im.height, int((y + h) * S + 0.999)))
        crop = im.crop(box)
        if name.startswith('btn_'):
            out = crop
        else:
            bg = im.getpixel((box[0] + 1, box[1] + 1))
            bb = ink_bbox(crop, 330, (255, 255, 255)) if name.startswith('o_') else ink_bbox(crop)
            if bb:
                crop = crop.crop(bb)
            ink_h = crop.height
            H = max(int(ink_h * 1.4), ink_h + 6)
            pad_x = max(3, int(ink_h * 0.2))
            out = Image.new('RGB', (crop.width + 2 * pad_x, H), bg if name.startswith('menu_') else 'white')
            out.paste(crop, (pad_x, (H - ink_h) // 2))
        out.save(os.path.join(ICONS, name + '.png'))
        print('icon', name, out.size)


if __name__ == '__main__':
    main()
