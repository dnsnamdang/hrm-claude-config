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
    """So do use case tong quan.

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

    has_note = any(u[3] for u in usecases)
    rx = int(255 * S) if has_note else int(295 * S)
    bx0 = int(430 * S)
    ucx = bx0 + int(40 * S) + rx
    # Khong co cot ghi chu -> khung he thong om sat ellipse, tieu de moi can giua dung
    bx1 = int(1465 * S) if has_note else ucx + rx + int(40 * S)
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

    CHIEU MUI TEN (chuan UML, sua 24/08/2026):
      include : base ──▶ sub   (use case me tro sang use case duoc include)
      extend  : sub  ──▶ base  (use case mo rong tro NGUOC ve use case me)
    """
    # Khong co include/extend -> thu hep khung, khong de khoang trang ben phai
    W = (1350 if relations else 760) * S
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
            # extend: mui ten tro NGUOC ve use case me (p1); include: tro sang sub (p2)
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


# ======================================================================
def draw_overview_rel(out_path, title, actor_name, nodes, relations=(),
                      actor_links=None, target_w=2200):
    """So do Use Case tong quan CO quan he «include» / «extend» giua cac use case.

    Khac `draw_overview` (chi 1 cot doc, khong ve quan he): ham nay bay 2 cot —
    cot GIUA la use case chinh (actor noi vao), cot PHAI la use case phu
    (use case duoc include, hoac use case mo rong).

    nodes     : [(id, nhan, nhom, cot), ...] voi cot in {'main', 'side'}
                `nhan` PHAI la cum dong tu (vd 'Xem danh sach quoc gia').
    relations : [(id_nguon, id_dich, kieu), ...] voi kieu in {'include','extend'}
                Huong theo dung chuan UML — nguon la dau mui ten di RA:
                  include : (base, sub)  -> mui ten tro sang sub
                  extend  : (sub,  base) -> mui ten tro nguoc ve base
    actor_links: danh sach id duoc noi voi actor; None = moi node cot 'main'.
    """
    main = [n for n in nodes if n[3] == 'main']
    side = [n for n in nodes if n[3] == 'side']
    if actor_links is None:
        actor_links = [n[0] for n in main]

    ry = 34 * S
    gap = 24 * S
    top_pad = 132 * S
    bot_pad = 52 * S
    W = 1900 * S

    def col_h(n):
        return n * (2 * ry) + max(0, n - 1) * gap

    inner_h = max(col_h(len(main)), col_h(len(side)))
    H = int(top_pad + inner_h + bot_pad)

    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)

    f_title = _f(F_BOLD, 20)
    f_uc = _f(F_REG, 15)
    f_actor = _f(F_BOLD, 15)
    f_rel = _f(F_ITAL, 13)

    rx = int(250 * S)
    cx_main = int(640 * S)
    cx_side = int(1560 * S)
    bx0, bx1 = int(330 * S), int(1870 * S)
    by0, by1 = int(58 * S), H - int(18 * S)
    _dashed_line(d, (bx0, by0), (bx1, by0), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx0, by1), (bx1, by1), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx0, by0), (bx0, by1), BOUND, max(3, int(2 * S)))
    _dashed_line(d, (bx1, by0), (bx1, by1), BOUND, max(3, int(2 * S)))

    tw, _ = _tw(d, title, f_title)
    d.text(((bx0 + bx1) / 2 - tw / 2, by0 + int(16 * S)), title, font=f_title, fill=INK)

    # moi cot tu can giua theo chieu doc trong vung `inner_h`
    pos = {}
    for col, cx in ((main, cx_main), (side, cx_side)):
        y = top_pad + (inner_h - col_h(len(col))) / 2 + ry
        for nid, label, grp, _c in col:
            _usecase(d, cx, y, rx, ry, label, grp, f_uc)
            pos[nid] = (cx, y)
            y += 2 * ry + gap

    # actor
    ay_center = top_pad + inner_h / 2
    ax, ay = _actor(d, int(150 * S), int(ay_center - 62 * S), actor_name, f_actor)
    for nid in actor_links:
        cx, cy = pos[nid]
        d.line([(ax + int(6 * S), ay), (cx - rx - int(4 * S), cy)],
               fill=(148, 163, 184), width=max(2, int(1.4 * S)))

    # quan he include / extend — luon ve giua canh phai cot main va canh trai cot side
    col_rel = (100, 116, 139)
    wid = max(2, int(1.6 * S))
    for src, dst, kind in relations:
        (sx, sy), (dx, dy) = pos[src], pos[dst]
        m, s = (src, dst) if sx == cx_main else (dst, src)
        pm, ps = pos[m], pos[s]
        p_main = (pm[0] + rx + int(14 * S), pm[1])
        p_side = (ps[0] - rx - int(12 * S), ps[1])
        _dashed_line(d, p_main, p_side, col_rel, wid)
        # dau mui ten dat o DICH
        if dst == m:
            _arrow_head(d, p_side, p_main, col_rel, wid)
        else:
            _arrow_head(d, p_main, p_side, col_rel, wid)
        # nhan dat gan DAU DUONG (phia use case nguon) de 8 duong khong de nhan len nhau
        p_src = p_main if src == m else p_side
        p_dst = p_side if src == m else p_main
        lx = p_src[0] + (p_dst[0] - p_src[0]) * 0.26
        ly = p_src[1] + (p_dst[1] - p_src[1]) * 0.26 - int(20 * S)
        lbl = '«%s»' % kind
        lw, lh = _tw(d, lbl, f_rel)
        d.rectangle([lx - lw / 2 - 5 * S, ly - lh / 2 - 9 * S,
                     lx + lw / 2 + 5 * S, ly + lh / 2 + 7 * S], fill='white')
        d.text((lx - lw / 2, ly - lh / 2 - 3 * S), lbl, font=f_rel, fill=(71, 85, 105))

    return _finish(img, out_path, target_w)
