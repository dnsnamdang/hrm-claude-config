# -*- coding: utf-8 -*-
"""Ảnh màn dài (nới khung nhìn) có dải trống lớn giữa nội dung và thanh nút cố định đáy -> cắt bớt dải trống.
Dùng: python crop_blank.py <ảnh>...   (chỉ cắt khi dải trống > 160 px, chừa lại 50 px)"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageStat

KEEP, MIN = 50, 160
for path in sys.argv[1:]:
    im = Image.open(path).convert('RGB')
    W, H = im.size
    x0, x1 = int(W * 0.2), int(W * 0.97)

    def blank(y):
        st = ImageStat.Stat(im.crop((x0, y, x1, y + 1)))
        return max(st.stddev) < 2.5

    # bỏ qua thanh nút đáy: dò từ đáy lên tới khi gặp dòng trống đầu tiên
    y = H - 1
    while y > 0 and blank(y):
        y -= 1
    while y > 0 and not blank(y):
        y -= 1
    end = y
    while y > 0 and blank(y):
        y -= 1
    start = y + 1
    gap = end - start + 1
    if gap > MIN:
        top = im.crop((0, 0, W, start + KEEP))
        bot = im.crop((0, end + 1, W, H))
        out = Image.new('RGB', (W, top.height + bot.height))
        out.paste(top, (0, 0))
        out.paste(bot, (0, top.height))
        out.save(path)
        print('cắt %d px: %s' % (gap - KEEP, path))
    else:
        print('giữ nguyên: %s' % path)
