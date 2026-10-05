# -*- coding: utf-8 -*-
"""Cắt sát ảnh nút/icon cho HDSD: bỏ khoảng trắng thừa quanh nút, chừa đúng PAD px.

Khuôn chuẩn (HDSD_MAU_GON.docx): ảnh nút ôm sát viền nút, dư 0–2 px. Chụp bằng boundingBox ± vài px
hay bị dính nền trang / ô bảng xung quanh → ảnh chèn cao 0,22" sẽ làm nút bé lại và lệch dòng chữ.

Cách dùng:
    python3 trim_icon.py <file_hoặc_thư_mục> [...]          # cắt thẳng vào file
    python3 trim_icon.py --dry <thư_mục>                     # chỉ liệt kê file còn dư
"""
import os
import sys

from PIL import Image, ImageChops

PAD = 2          # px chừa lại quanh nút
PAD_DARK = 6     # mục menu nền tối không có viền → chừa rộng hơn chút cho khỏi dính mép
TOL = 12         # chênh màu tối thiểu coi là "không phải nền" (viền xám nhạt #dee2e6 vẫn giữ được)
MAX_OK = 3       # dư <= MAX_OK px thì coi là đã sát (đúng mức của file mẫu)
MIN_H = 26       # mục không viền (mục menu) cắt sát chữ sẽ bị phóng to khi chèn cao 0,22" → bù nền cho đủ cao


def _bg(im):
    """Màu nền = màu xuất hiện nhiều nhất ở 4 góc."""
    w, h = im.size
    cs = [im.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    return max(set(cs), key=cs.count)


TOL_DARK = 70    # nền TỐI (menu sidebar có hoa văn/dải màu): chỉ chữ + icon sáng mới là nội dung


def _is_dark(c):
    return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) < 110


def bbox(im):
    im = im.convert('RGB')
    bg = _bg(im)
    diff = ImageChops.difference(im, Image.new('RGB', im.size, bg)).convert('L')
    tol = TOL_DARK if _is_dark(bg) else TOL
    return diff.point(lambda v: 255 if v > tol else 0).getbbox()


def trim(path, dry=False):
    im = Image.open(path)
    bb = bbox(im)
    if not bb:
        return None
    w, h = im.size
    m = (bb[0], bb[1], w - bb[2], h - bb[3])
    # ảnh đã đúng chiều cao tối thiểu thì phần nền trên/dưới là phần bù cố ý, chỉ xét 2 bên
    check = m if h > MIN_H else (m[0], 0, m[2], 0)
    lim = PAD_DARK + 1 if _is_dark(_bg(im.convert('RGB'))) else MAX_OK
    if max(check) <= lim:
        return None
    pad = PAD_DARK if _is_dark(_bg(im.convert('RGB'))) else PAD
    box = (max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, w), min(bb[3] + pad, h))
    out = im.convert('RGB').crop(box)
    if out.height < MIN_H:
        canvas = Image.new('RGB', (out.width, MIN_H), _bg(im.convert('RGB')))
        canvas.paste(out, (0, (MIN_H - out.height) // 2))
        out = canvas
    if not dry:
        out.save(path)
    return m, (w, h), out.size


def main(args):
    dry = '--dry' in args
    files = []
    for a in (x for x in args if x != '--dry'):
        if os.path.isdir(a):
            files += sorted(os.path.join(a, f) for f in os.listdir(a) if f.lower().endswith('.png'))
        else:
            files.append(a)
    n = 0
    for f in files:
        r = trim(f, dry)
        if r:
            n += 1
            print('%s  dư(trái,trên,phải,dưới)=%s  %s -> %s' % (os.path.basename(f), r[0], r[1], r[2]))
    print('%s %d/%d file' % ('Cần cắt' if dry else 'Đã cắt', n, len(files)))


if __name__ == '__main__':
    main(sys.argv[1:])
