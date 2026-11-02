# -*- coding: utf-8 -*-
"""Sơ đồ luồng trạng thái phiếu Yêu cầu mua dịch vụ — 2 hàng, đủ mọi nhánh (viết riêng trong thư mục này vì
`_lib_phieu.draw_state_flow` chỉ vẽ 1 hàng, không đủ chỗ cho 9 trạng thái). Không sửa lib chung."""
import os
from PIL import Image, ImageDraw, ImageFont

FD = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
F_BOX = ImageFont.truetype(os.path.join(FD, 'timesbd.ttf'), 40)
F_LBL = ImageFont.truetype(os.path.join(FD, 'times.ttf'), 32)

W, H = 3150, 900
BW, BH = 340, 130
# mã: (tâm x, tâm y, nhãn, màu nền) — 'start' / 'end' là chấm tròn
NODES = {
    'S': (90, 280, '', None),
    'A': (430, 280, 'Đang tạo', '#e5e7eb'),
    'B': (1050, 280, 'Chờ TP duyệt', '#fef3c7'),
    'C': (1670, 280, 'Chờ KS duyệt', '#fef3c7'),
    'D': (2290, 280, 'Đã duyệt', '#dcfce7'),
    'E': (2920, 280, 'Đang lập / Đã lập hợp đồng', '#dcfce7'),
    'X': (430, 740, '', 'end'),
    'K': (1360, 740, 'Không duyệt', '#fee2e2'),
    'Hy': (2290, 740, 'Hủy', '#fee2e2'),
}


def _box(d, code):
    x, y, label, color = NODES[code]
    if code == 'S' or color == 'end':
        r = 24
        d.ellipse([x - r, y - r, x + r, y + r], fill='#111827')
        if color == 'end':
            d.ellipse([x - r - 9, y - r - 9, x + r + 9, y + r + 9], outline='#111827', width=4)
            d.text((x + 50, y - 20), 'Đã xóa', font=F_BOX, fill='#0f172a')
        return
    words, lines, cur = label.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=F_BOX) <= BW - 40 or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    lines.append(cur)
    d.rounded_rectangle([x - BW / 2, y - BH / 2, x + BW / 2, y + BH / 2], radius=26, fill=color, outline='#334155', width=3)
    for k, s in enumerate(lines):
        ty = y - 24 * len(lines) + 48 * k
        d.text((x - d.textlength(s, font=F_BOX) / 2, ty), s, font=F_BOX, fill='#0f172a')


def _arrow_head(d, p, q, color):
    import math
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    s = 22
    a1 = (q[0] - s * math.cos(ang - 0.45), q[1] - s * math.sin(ang - 0.45))
    a2 = (q[0] - s * math.cos(ang + 0.45), q[1] - s * math.sin(ang + 0.45))
    d.polygon([q, a1, a2], fill=color)


def _path(d, pts, label, color='#475569', lpos=None, lcolor='#1e3a8a'):
    d.line(pts, fill=color, width=4)
    _arrow_head(d, pts[-2], pts[-1], color)
    if label:
        if lpos is None:
            i = len(pts) // 2
            a, b = pts[i - 1], pts[i]
            lpos = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        tw = d.textlength(label, font=F_LBL)
        x, y = lpos
        d.rectangle([x - tw / 2 - 6, y - 20, x + tw / 2 + 6, y + 20], fill='white')
        d.text((x - tw / 2, y - 18), label, font=F_LBL, fill=lcolor)


def draw(path):
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    N = NODES
    L = lambda c: N[c][0] - BW / 2  # noqa: E731
    R = lambda c: N[c][0] + BW / 2  # noqa: E731
    T = lambda c: N[c][1] - BH / 2  # noqa: E731
    Bo = lambda c: N[c][1] + BH / 2  # noqa: E731
    y0 = N['A'][1]
    # hàng chính
    _path(d, [(N['S'][0] + 26, y0), (L('A') - 4, y0)], '', '#475569')
    d.text((N['S'][0] - 30, y0 + 40), 'Lưu nháp', font=F_LBL, fill='#1e3a8a')
    _path(d, [(R('A') + 4, y0), (L('B') - 4, y0)], 'Gửi duyệt', lpos=((R('A') + L('B')) / 2, y0 - 34))
    _path(d, [(R('B') + 4, y0), (L('C') - 4, y0)], 'TP duyệt', lpos=((R('B') + L('C')) / 2, y0 - 34))
    _path(d, [(R('C') + 4, y0), (L('D') - 4, y0)], 'KS duyệt giá', lpos=((R('C') + L('D')) / 2, y0 - 34))
    _path(d, [(R('D') + 4, y0), (L('E') - 4, y0)], 'Lập hợp đồng', lpos=((R('D') + L('E')) / 2, y0 - 34))
    d.text(((R('D') + L('E')) / 2 - 75, y0 + 22), '(ngoài HRM)', font=F_LBL, fill='#64748b')
    # lập mới gửi duyệt luôn: vòng trên
    yt = 90
    _path(d, [(N['S'][0], y0 - 26), (N['S'][0], yt), (N['B'][0] - 60, yt), (N['B'][0] - 60, T('B') - 4)],
          'Gửi duyệt ngay khi lập', '#475569', lpos=((N['S'][0] + N['B'][0]) / 2, yt))
    # duyệt lại giá: vòng trên D -> C
    _path(d, [(N['D'][0], T('D') - 4), (N['D'][0], yt), (N['C'][0] + 60, yt), (N['C'][0] + 60, T('C') - 4)],
          'Yêu cầu duyệt lại giá', '#b45309', lpos=((N['C'][0] + N['D'][0]) / 2, yt), lcolor='#92400e')
    # hủy
    _path(d, [(N['D'][0], Bo('D') + 4), (N['D'][0], T('Hy') - 4)], 'Hủy yêu cầu', '#b91c1c',
          lpos=(N['D'][0], (Bo('D') + T('Hy')) / 2), lcolor='#991b1b')
    # từ chối
    _path(d, [(N['B'][0] - 20, Bo('B') + 4), (N['K'][0] - 150, T('K') - 4)], 'Từ chối', '#b91c1c', lcolor='#991b1b',
          lpos=((N['B'][0] - 20 + N['K'][0] - 150) / 2 - 80, (Bo('B') + T('K')) / 2))
    _path(d, [(N['C'][0] - 20, Bo('C') + 4), (N['K'][0] + 150, T('K') - 4)], 'Từ chối', '#b91c1c', lcolor='#991b1b',
          lpos=((N['C'][0] - 20 + N['K'][0] + 150) / 2 + 70, (Bo('C') + T('K')) / 2))
    # sửa lại
    _path(d, [(N['K'][0] - 40, T('K') - 4), (N['B'][0] + 120, Bo('B') + 4)], 'Sửa, gửi duyệt', '#047857',
          lcolor='#065f46', lpos=((N['K'][0] - 40 + N['B'][0] + 120) / 2 + 40, (Bo('B') + T('K')) / 2 + 40))
    _path(d, [(L('K') - 4, N['K'][1] - 30), (R('A') - 40, Bo('A') + 4)], 'Lưu nháp', '#047857', lcolor='#065f46',
          lpos=((L('K') + R('A') - 40) / 2 - 30, (N['K'][1] - 30 + Bo('A')) / 2))
    # xóa
    _path(d, [(N['A'][0], Bo('A') + 4), (N['X'][0], N['X'][1] - 36)], 'Xóa', '#b91c1c', lcolor='#991b1b',
          lpos=(N['A'][0] - 50, (Bo('A') + N['X'][1]) / 2))
    _path(d, [(L('K') - 4, N['K'][1] + 30), (N['X'][0] + 36, N['K'][1] + 30)], 'Xóa', '#b91c1c', lcolor='#991b1b',
          lpos=((L('K') + N['X'][0]) / 2 + 120, N['K'][1] + 30))
    for code in NODES:
        _box(d, code)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path


if __name__ == '__main__':
    print(draw(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uml', 'state_flow.png')))
