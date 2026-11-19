#!/usr/bin/env python3
"""In chữ trên màn máy ảo kèm toạ độ tâm (điểm 402×874): python3 tools/scr.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import vc
for x, y, w, h, t in sorted(vc.ocr(), key=lambda r: (round(r[1] / 6), r[0])):
    print(f'{round(x + w / 2):4d},{round(y + h / 2):4d}  {t}')
