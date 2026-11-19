"""Chỉnh bánh xe giờ Cupertino theo OCR: đọc giá trị ở hàng giữa (y≈731) rồi vuốt từng nấc."""
import re
from record import ocr, swipe, w, nz

BAND = (712, 752)


def read_col(d, colx, kind):
    for x, y, bw, bh, t in ocr(d):
        cy, cx = y + bh / 2, x + bw / 2
        if BAND[0] <= cy <= BAND[1] and abs(cx - colx) < 55:
            s = nz(t)
            if kind == 'date':
                if 'hom nay' in s:
                    return 1
                m = re.findall(r'\d+', s)
                return int(m[-1]) if m else None
            m = re.findall(r'\d+', s)
            if m:
                return int(m[0])
    return None


def set_wheel(d, colx, want, kind='num', tries=40):
    for _ in range(tries):
        cur = read_col(d, colx, kind)
        if cur is None:
            w(0.4); continue
        if cur == want:
            return True
        coarse = abs(cur - want) >= 5
        dist, dur = (60, 2000) if coarse else (30, 1500)
        if cur < want:
            swipe(d, colx, 760, colx, 760 - dist, dur)
        else:
            swipe(d, colx, 690, colx, 690 + dist, dur)
        w(0.9)
    return False
