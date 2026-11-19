# -*- coding: utf-8 -*-
"""Cắt bớt khoảng trắng bên phải icon mục menu (menu_muc) — ô mục menu trong panel rộng ~460px CSS."""
import os
from PIL import Image
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdsd_shots', 'icons', 'menu_muc.png')
im = Image.open(p)
if im.width > 480:
    im.crop((0, 0, 470, im.height)).save(p)
print(Image.open(p).size)
