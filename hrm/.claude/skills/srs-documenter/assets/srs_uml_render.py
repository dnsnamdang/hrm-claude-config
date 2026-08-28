# -*- coding: utf-8 -*-
"""Ve bieu do Use Case (UML) ra file PNG bang Pillow, khong can trinh duyet.

Ve o ty le 3x roi thu nho bang LANCZOS -> vien muot, chu net khi chen vao Word.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = 3  # he so sieu lay mau

FONT_DIR = r'C:\Windows\Fonts'
F_REG = os.path.join(FONT_DIR, 'segoeui.ttf')
F_BOLD = os.path.join(FONT_DIR, 'segoeuib.ttf')
F_ITAL = os.path.join(FONT_DIR, 'segoeuii.ttf')

INK = (15, 23, 42)
MUTED = (100, 116, 139)
BOUND = (100, 116, 139)

# bang mau theo nhom chuc nang
PALETTE = {
    'view':   ((219, 234, 254), (29, 78, 216)),    # xanh duong
    'crud':   ((220, 252, 231), (21, 128, 61)),    # xanh la
    'action': ((254, 243, 199), (180, 83, 9)),     # cam
    'io':     ((243, 232, 255), (126, 34, 206)),   # tim
    'sub':    ((241, 245, 249), (71, 85, 105)),    # xam - dung cho include/extend
}


def _f(path, size):
    return ImageFont.truetype(path, int(size * S))


def _tw(d, txt, font):
    b = d.textbbox((0, 0), txt, font=font)
    return b[2] - b[0], b[3] - b[1]


def _wrap(d, txt, font, max_w):
    """Ngat dong theo be rong toi da (px o ty le S)."""
    words = txt.split()
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if _tw(d, t, font)[0] <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _center_text(d, cx, cy, lines, font, fill, lh=None):
    if lh is None:
        lh = _tw(d, 'Ag', font)[1] + 7 * S
    total = lh * len(lines)
    y = cy - total / 2
    for ln in lines:
        w, h = _tw(d, ln, font)
        d.text((cx - w / 2, y), ln, font=font, fill=fill)
        y += lh


def _dashed_line(d, p1, p2, fill, width, dash=9 * S, gap=6 * S):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = (dx * dx + dy * dy) ** 0.5
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    pos = 0.0
    while pos < dist:
        e = min(pos + dash, dist)
        d.line([(x1 + ux * pos, y1 + uy * pos), (x1 + ux * e, y1 + uy * e)], fill=fill, width=width)
        pos = e + gap


def _arrow_head(d, p_from, p_to, fill, width, size=13):
    """Mui ten mo (2 vach) o dau p_to."""
    import math
    x1, y1 = p_from
    x2, y2 = p_to
    ang = math.atan2(y2 - y1, x2 - x1)
    L = size * S
    for a in (ang + math.radians(160), ang - math.radians(160)):
        d.line([(x2, y2), (x2 + L * math.cos(a), y2 + L * math.sin(a))], fill=fill, width=width)


def _actor(d, cx, top, label, font, scale=1.0):
    """Ve hinh nguoi que + nhan ben duoi. Tra ve (x_phai, y_giua_than)."""
    r = int(15 * S * scale)
    body = int(48 * S * scale)
    arm = int(24 * S * scale)
    leg = int(26 * S * scale)
    w = max(3, int(2.6 * S))
    hy = top + r
    d.ellipse([cx - r, top, cx + r, top + 2 * r], outline=INK, width=w)
    d.line([(cx, top + 2 * r), (cx, top + 2 * r + body)], fill=INK, width=w)
    ay = top + 2 * r + int(body * 0.32)
    d.line([(cx - arm, ay), (cx + arm, ay)], fill=INK, width=w)
    fy = top + 2 * r + body
    d.line([(cx, fy), (cx - int(arm * 0.85), fy + leg)], fill=INK, width=w)
    d.line([(cx, fy), (cx + int(arm * 0.85), fy + leg)], fill=INK, width=w)
    lines = _wrap(d, label, font, int(160 * S * scale))
    _center_text(d, cx, fy + leg + int(20 * S * scale) + (len(lines) - 1) * 8 * S, lines, font, INK)
    return cx + arm, ay


def _usecase(d, cx, cy, rx, ry, text, group, font, sub=None):
    """Ve ellipse use case. Tra ve (x_trai, x_phai)."""
    fill, stroke = PALETTE.get(group, PALETTE['crud'])
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=stroke, width=max(3, int(1.8 * S)))
    lines = _wrap(d, text, font, int(rx * 1.62))
    if sub:
        lines = lines + [sub]
    _center_text(d, cx, cy, lines, font, INK)
    return cx - rx, cx + rx


def _finish(img, out_path, target_w):
    img = img.resize((target_w, int(img.height * target_w / img.width)), Image.LANCZOS)
    img.save(out_path, 'PNG')
    return out_path


# ======================================================================
def draw_overview(out_path, title, actors, usecases, target_w=2000):
    """FORM CU (truoc 2026-08-28) — so do use case tong quan PHANG.

    Moi use case mot ellipse ngang hang, cai nao cung noi thang toi actor. Tai lieu moi
    dung `draw_overview2()`: chi man hinh that moi noi toi actor, thao tac tren man do
    noi bang «include»/«extend». Giu ham nay de cac gen_srs.py cu chay lai duoc.

    actors:   [(ten_actor, [chi_so_usecase, ...]), ...]
    usecases: [(ma, ten, nhom, ghi_chu_hoac_None), ...]
    """
    n = len(usecases)
    ry = 34 * S
    gap = 22 * S
    top_pad = 132 * S          # chua tieu de, khong de de len ellipse dau tien
    bot_pad = 52 * S
    W = 1500 * S
    inner_h = n * (2 * ry) + (n - 1) * gap
    H = int(top_pad + inner_h + bot_pad)

    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)

    f_title = _f(F_BOLD, 20)
    f_uc = _f(F_REG, 15)
    f_actor = _f(F_BOLD, 15)
    f_note = _f(F_ITAL, 12.5)

    bx0, bx1 = int(430 * S), int(1465 * S)
    by0, by1 = int(58 * S), H - int(18 * S)
    # khung he thong (net dut)
    for i in range(4):
        pass
    _dashed_line(d, (bx0, by0), (bx1, by0), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx0, by1), (bx1, by1), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx0, by0), (bx0, by1), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx1, by0), (bx1, by1), BOUND, max(3, int(2 * S)))

    tw, _ = _tw(d, title, f_title)
    d.text(((bx0 + bx1) / 2 - tw / 2, by0 + int(16 * S)), title, font=f_title, fill=INK)

    has_note = any(u[3] for u in usecases)
    rx = int(255 * S) if has_note else int(295 * S)
    ucx = bx0 + int(40 * S) + rx
    note_x = ucx + rx + int(20 * S)
    note_w = bx1 - int(20 * S) - note_x
    pos = []
    y = top_pad + ry
    for code, name, grp, note in usecases:
        left, right = _usecase(d, ucx, y, rx, ry, '%s  %s' % (code, name), grp, f_uc)
        if note:
            nl = _wrap(d, note, f_note, note_w)
            _center_text(d, note_x + note_w / 2, y, nl, f_note, MUTED)
        pos.append((left, y))
        y += 2 * ry + gap

    # actors ben trai
    na = len(actors)
    span = inner_h
    for i, (aname, idxs) in enumerate(actors):
        ay_center = top_pad + span * (i + 0.5) / na
        ax, ay = _actor(d, int(210 * S), int(ay_center - 62 * S), aname, f_actor)
        for j in idxs:
            lx, ly = pos[j]
            d.line([(ax + int(6 * S), ay), (lx - int(4 * S), ly)], fill=(148, 163, 184), width=max(2, int(1.4 * S)))

    return _finish(img, out_path, target_w)


def draw_usecase(out_path, actor_name, main_code, main_name, main_group,
                 relations=(), target_w=1700):
    """So do use case cho 1 chuc nang.

    relations: [(kieu, ten), ...] voi kieu in {'include','extend'}
    """
    W = 1350 * S
    rows = max(1, len(relations))
    row_h = 128 * S
    H = int(max(240 * S, 46 * S + rows * row_h))

    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)

    f_uc = _f(F_REG, 15)
    f_actor = _f(F_BOLD, 15)
    f_rel = _f(F_ITAL, 13)
    f_sub = _f(F_REG, 14)

    cy = H / 2
    ax, ay = _actor(d, int(120 * S), int(cy - 62 * S), actor_name, f_actor)

    mx = int(500 * S)
    mrx, mry = int(190 * S), int(48 * S)
    mleft, mright = _usecase(d, mx, cy, mrx, mry, '%s  %s' % (main_code, main_name), main_group, f_uc)
    d.line([(ax + int(6 * S), ay), (mleft - int(4 * S), cy)], fill=(148, 163, 184), width=max(2, int(1.4 * S)))

    if relations:
        sx = int(1030 * S)
        srx, sry = int(210 * S), int(42 * S)
        y0 = cy - (len(relations) - 1) * row_h / 2
        for k, (kind, name) in enumerate(relations):
            yy = y0 + k * row_h
            sleft, _ = _usecase(d, sx, yy, srx, sry, name, 'sub', f_sub)
            p1 = (mright + int(14 * S), cy)
            p2 = (sleft - int(12 * S), yy)
            _dashed_line(d, p1, p2, (100, 116, 139), max(2, int(1.6 * S)))
            # Chieu mui ten theo dung chuan UML:
            #   «include» : use case CHINH -> use case duoc goi   (p1 -> p2)
            #   «extend»  : use case MO RONG -> use case CO SO    (p2 -> p1)
            if kind == 'extend':
                _arrow_head(d, p2, p1, (100, 116, 139), max(2, int(1.6 * S)))
            else:
                _arrow_head(d, p1, p2, (100, 116, 139), max(2, int(1.6 * S)))
            # Nhan dat PHIA TREN duong noi de khong cat qua net dut
            lbl = '«%s»' % kind
            lw, lh = _tw(d, lbl, f_rel)
            mcx = (p1[0] + p2[0]) / 2
            mcy = (p1[1] + p2[1]) / 2 - int(24 * S)
            d.rectangle([mcx - lw / 2 - 5 * S, mcy - lh / 2 - 9 * S,
                         mcx + lw / 2 + 5 * S, mcy + lh / 2 + 7 * S], fill='white')
            d.text((mcx - lw / 2, mcy - lh / 2 - 3 * S), lbl, font=f_rel, fill=(71, 85, 105))

    return _finish(img, out_path, target_w)


def draw_overview2(out_path, actors, mains, subs, target_w=2000):
    """So do use case tong quan CO PHAN CAP — ban dung tu 2026-08-28.

    Chi use case la MAN HINH that su moi noi thang toi actor; cac thao tac lam ngay tren
    man do (loc, tuy chinh cot, xoa, in, lich su, popup chon du lieu...) phai noi vao use
    case cha bang «include» / «extend». Khung he thong KHONG co dong tieu de.

    actors : [(ten_actor, [chi_so_main, ...]), ...]
    mains  : [(ma, ten, nhom), ...]
    subs   : [(ma, ten, nhom, kieu, [chi_so_main, ...], ghi_chu|None), ...]
             kieu in {'include', 'extend'}; sub xep vao block cua main DAU TIEN no tro toi.
             `ghi_chu` hien KHONG duoc ve (user chot bo cot ghi chu ben phai) — van giu
             trong du lieu vi dieu kien do da noi o ma tran phan quyen / Phan 4.
    """
    # ---- gan moi sub vao block cua main dau tien no tro toi
    blocks = []                       # [(main_idx, [sub_idx, ...])]
    for i in range(len(mains)):
        blocks.append((i, [k for k, s in enumerate(subs) if s[4][0] == i]))
    rows_total = sum(max(1, len(b[1])) for b in blocks)

    ry_m, ry_s = int(36 * S), int(33 * S)
    row_h = int(102 * S)
    top_pad, bot_pad = int(46 * S), int(40 * S)
    W = int(1290 * S)
    H = int(top_pad + rows_total * row_h + bot_pad)

    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)

    f_uc = _f(F_REG, 14)
    f_sub = _f(F_REG, 13.5)
    f_actor = _f(F_BOLD, 15)
    f_rel = _f(F_ITAL, 12.5)

    bx0, bx1 = int(372 * S), int(1262 * S)
    by0, by1 = int(20 * S), H - int(16 * S)
    line_w = max(3, int(2 * S))
    _dashed_line(d, (bx0, by0), (bx1, by0), BOUND, line_w)
    _dashed_line(d, (bx0, by1), (bx1, by1), BOUND, line_w)
    _dashed_line(d, (bx0, by0), (bx0, by1), BOUND, line_w)
    _dashed_line(d, (bx1, by0), (bx1, by1), BOUND, line_w)

    rx_m, rx_s = int(190 * S), int(182 * S)
    mx = bx0 + int(28 * S) + rx_m
    sx = bx1 - int(24 * S) - rx_s

    # ---- ve theo tung block
    m_pos = [None] * len(mains)       # (x_trai, x_phai, y) cua use case chinh
    s_pos = [None] * len(subs)
    y = top_pad
    for mi, sub_ids in blocks:
        n = max(1, len(sub_ids))
        block_top = y
        for k, si in enumerate(sub_ids):
            sy = block_top + row_h * k + row_h / 2
            code, name, grp, kind, parents, note = subs[si]
            left, right = _usecase(d, sx, sy, rx_s, ry_s,
                                     '%s  %s' % (code, name), grp, f_sub)
            s_pos[si] = (left, right, sy)
        my = block_top + row_h * n / 2
        code, name, grp = mains[mi]
        left, right = _usecase(d, mx, my, rx_m, ry_m, '%s  %s' % (code, name), grp, f_uc)
        m_pos[mi] = (left, right, my)
        y = block_top + row_h * n

    # ---- duong «include» / «extend» tu use case cha sang use case phu
    grey = (100, 116, 139)
    w_rel = max(2, int(1.6 * S))
    # moi use case cha co the nhan nhieu duong -> tach diem neo theo hang cho khoi chong
    fan = {}
    for si, s in enumerate(subs):
        for pi in s[4]:
            fan.setdefault(pi, []).append(si)

    for si, (code, name, grp, kind, parents, note) in enumerate(subs):
        sleft, _sright, sy = s_pos[si]
        for pi in parents:
            _pl, pright, py = m_pos[pi]
            sib = fan[pi]
            off = (sib.index(si) - (len(sib) - 1) / 2.0) * int(13 * S)
            p1 = (pright + int(12 * S), py + off)
            p2 = (sleft - int(12 * S), sy)
            _dashed_line(d, p1, p2, grey, w_rel)
            # Chieu mui ten theo dung chuan UML:
            #   «include» : use case CHA -> use case duoc goi   (p1 -> p2)
            #   «extend»  : use case MO RONG -> use case CO SO  (p2 -> p1)
            if kind == 'extend':
                _arrow_head(d, p2, p1, grey, w_rel)
            else:
                _arrow_head(d, p1, p2, grey, w_rel)
            lbl = '«%s»' % kind
            lw, lh = _tw(d, lbl, f_rel)
            cx = (p1[0] + p2[0]) / 2
            cy = (p1[1] + p2[1]) / 2 - int(20 * S)
            d.rectangle([cx - lw / 2 - 5 * S, cy - lh / 2 - 9 * S,
                         cx + lw / 2 + 5 * S, cy + lh / 2 + 7 * S], fill='white')
            d.text((cx - lw / 2, cy - lh / 2 - 3 * S), lbl, font=f_rel, fill=(71, 85, 105))

    # ---- actor ben trai, chi noi toi use case CHINH
    na = len(actors)
    inner_h = rows_total * row_h
    for i, (aname, idxs) in enumerate(actors):
        ay_center = top_pad + inner_h * (i + 0.5) / na
        ax, ay = _actor(d, int(180 * S), int(ay_center - 62 * S), aname, f_actor)
        for j in idxs:
            lx, _r, ly = m_pos[j]
            d.line([(ax + int(6 * S), ay), (lx - int(4 * S), ly)],
                   fill=(148, 163, 184), width=max(2, int(1.4 * S)))

    return _finish(img, out_path, target_w)
