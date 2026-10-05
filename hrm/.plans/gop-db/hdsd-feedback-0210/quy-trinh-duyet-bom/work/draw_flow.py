# -*- coding: utf-8 -*-
"""Vẽ sơ đồ quy trình phê duyệt BOM list (Pillow, khổ dọc để đọc rõ trên A4) -> shots/00_so_do.png"""
import math
from PIL import Image, ImageDraw, ImageFont

OUT = '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/hdsd-feedback-0210/quy-trinh-duyet-bom/shots/00_so_do.png'
F = '/System/Library/Fonts/Supplemental/Arial.ttf'
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
f_box = ImageFont.truetype(F, 30)
f_boxb = ImageFont.truetype(FB, 30)
f_lane = ImageFont.truetype(FB, 31)
f_lbl = ImageFont.truetype(FB, 28)
f_st = ImageFont.truetype(FB, 26)
f_title = ImageFont.truetype(FB, 44)
f_note = ImageFont.truetype(F, 28)

LW = 440
X0 = 20
COLS = 4
W = X0 * 2 + LW * COLS
HEAD_Y, HEAD_H = 90, 120
ROW0, RS = HEAD_Y + HEAD_H + 130, 255
NROW = 8
BOT = ROW0 + (NROW - 1) * RS + 130
H = BOT + 150

lanes = ['Người lập BOM', 'Leader hạng mục', 'PM giải pháp', 'Người tạo giải pháp\n(trưởng phòng GP)']
LANE_BG = ['#EFF6FF', '#F5F3FF', '#ECFDF5', '#FFF7ED']
LANE_HD = ['#2563EB', '#7C3AED', '#16A34A', '#D97706']

img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)
d.text((W // 2, 48), 'SƠ ĐỒ QUY TRÌNH PHÊ DUYỆT BOM LIST', font=f_title, fill='#0F172A', anchor='mm')


def cx(c):
    return X0 + c * LW + LW // 2


def ry(r):
    return ROW0 + r * RS


for i, name in enumerate(lanes):
    x0 = X0 + i * LW
    d.rectangle([x0, HEAD_Y, x0 + LW, BOT], fill=LANE_BG[i], outline='#CBD5E1', width=2)
    d.rectangle([x0, HEAD_Y, x0 + LW, HEAD_Y + HEAD_H], fill=LANE_HD[i], outline='#CBD5E1', width=2)
    d.multiline_text((x0 + LW // 2, HEAD_Y + HEAD_H // 2), name, font=f_lane, fill='white',
                     anchor='mm', align='center', spacing=6)

BW, BH = 380, 170


def box(c, r, lines, status=None, color='#1E293B', fill='white'):
    x, y = cx(c), ry(r)
    x0, y0, x1, y1 = x - BW // 2, y - BH // 2, x + BW // 2, y + BH // 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=fill, outline=color, width=4)
    n = len(lines) + (1 if status else 0)
    lh = 36
    ty = y - (n - 1) * lh / 2
    for k, t in enumerate(lines):
        d.text((x, ty + k * lh), t, font=f_boxb if k == 0 else f_box, fill='#0F172A', anchor='mm')
    if status:
        txt, col = status
        tw = d.textlength(txt, font=f_st) + 24
        sy = ty + len(lines) * lh + 2
        d.rounded_rectangle([x - tw / 2, sy - 16, x + tw / 2, sy + 16], radius=14, fill=col)
        d.text((x, sy), txt, font=f_st, fill='white', anchor='mm')
    return (x0, y0, x1, y1)


DW, DH = 340, 190


def diamond(c, r, lines, color):
    x, y = cx(c), ry(r)
    pts = [(x, y - DH // 2), (x + DW // 2, y), (x, y + DH // 2), (x - DW // 2, y)]
    d.polygon(pts, fill='white')
    d.line(pts + [pts[0]], fill=color, width=4)
    lh = 34
    ty = y - (len(lines) - 1) * lh / 2
    for k, t in enumerate(lines):
        d.text((x, ty + k * lh), t, font=f_boxb, fill='#0F172A', anchor='mm')


def arrow(pts, color='#334155', label=None, lpos=None):
    d.line(pts, fill=color, width=4, joint='curve')
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    L = 22
    p1 = (x2 - L * math.cos(a - 0.45), y2 - L * math.sin(a - 0.45))
    p2 = (x2 - L * math.cos(a + 0.45), y2 - L * math.sin(a + 0.45))
    d.polygon([(x2, y2), p1, p2], fill=color)
    if label:
        lx, ly = lpos
        tw = d.textlength(label, font=f_lbl) + 20
        d.rounded_rectangle([lx - tw / 2, ly - 19, lx + tw / 2, ly + 19], radius=10, fill='white',
                            outline=color, width=3)
        d.text((lx, ly), label, font=f_lbl, fill=color, anchor='mm')


S_HT = ('Hoàn thành', '#16A34A')
S_CD = ('Chờ duyệt', '#D97706')
S_DD = ('Đã duyệt', '#16A34A')
S_KD = ('Không duyệt', '#DC2626')
RED, GREEN = '#DC2626', '#16A34A'

A = box(0, 0, ['1. Tạo BOM', 'thành phần', '→ Lưu BOM'], S_HT)
B = box(0, 1, ['2. Tạo BOM tổng hợp', 'cấp hạng mục', '(gộp BOM thành phần)'], S_HT)
C = box(1, 2, ['3. Tạo hồ sơ trình', 'duyệt hạng mục', '→ Lưu & Trình duyệt'], S_CD)
diamond(2, 3, ['4. PM duyệt', 'hồ sơ hạng mục'], GREEN)
E = box(0, 3, ['5. Xem lý do từ chối,', 'Sao chép BOM, bổ sung', '→ Lưu BOM'], S_KD, color=RED)
Fb = box(0, 4, ['6. Tạo BOM tổng hợp', 'cấp giải pháp', '(gộp BOM hạng mục)'], S_HT)
G = box(2, 5, ['7. Tạo hồ sơ trình', 'duyệt giải pháp', '→ Lưu & Trình duyệt'], S_CD)
diamond(3, 6, ['8. Duyệt hồ sơ', 'giải pháp'], '#D97706')
K = box(0, 6, ['Xem lý do từ chối,', 'Sao chép BOM,', 'điều chỉnh → Lưu BOM'], S_KD, color=RED)
I = box(3, 7, ['BOM tổng hợp', 'cấp giải pháp', 'dùng lập báo giá'], S_DD, color=GREEN, fill='#F0FDF4')

# 1 -> 2
arrow([(cx(0), A[3]), (cx(0), B[1])])
# 2 -> 3
arrow([(B[2], ry(1)), (cx(1), ry(1)), (cx(1), C[1])])
# 3 -> 4
arrow([(C[2], ry(2)), (cx(2), ry(2)), (cx(2), ry(3) - DH // 2)])
# 4 Từ chối -> 5
arrow([(cx(2) - DW // 2, ry(3)), (E[2], ry(3))], RED, 'Từ chối', ((cx(2) - DW // 2 + E[2]) / 2, ry(3) - 32))
# 5 -> 3 gửi lại
arrow([(cx(0) + 60, E[1]), (cx(0) + 60, ry(2)), (C[0], ry(2))], RED, 'Gửi lại', (cx(0) + 60, ry(2) + 75))
# 4 Duyệt -> 6
arrow([(cx(2), ry(3) + DH // 2), (cx(2), ry(4)), (Fb[2], ry(4))], GREEN, 'Duyệt', (cx(2), ry(3) + DH // 2 + 40))
# 6 -> 7
arrow([(cx(0) + 60, Fb[3]), (cx(0) + 60, ry(4) + 125), (cx(2), ry(4) + 125), (cx(2), G[1])])
# 7 -> 8
arrow([(G[2], ry(5)), (cx(3), ry(5)), (cx(3), ry(6) - DH // 2)])
# 8 Duyệt -> I
arrow([(cx(3), ry(6) + DH // 2), (cx(3), I[1])], GREEN, 'Duyệt', (cx(3) + 90, ry(6) + DH // 2 + 38))
# 8 Từ chối -> K
arrow([(cx(3) - DW // 2, ry(6)), (K[2], ry(6))], RED, 'Từ chối', (cx(1) + 40, ry(6) - 32))
# K -> 7 gửi lại
arrow([(cx(0) - 60, K[1]), (cx(0) - 60, ry(5)), (G[0], ry(5))], RED, 'Gửi lại', (cx(1), ry(5) - 32))

notes = ['Giải pháp không chia hạng mục: bỏ bước 2 – 5, BOM tổng hợp cấp giải pháp gộp thẳng các BOM thành phần.',
         'Dự án tự triển khai: bước 7 bấm Lưu & Duyệt, BOM được duyệt ngay, không qua bước 8.']
for k, t in enumerate(notes):
    d.text((W // 2, BOT + 50 + k * 42), t, font=f_note, fill='#374151', anchor='mm')
img.save(OUT)
print(OUT, img.size)
