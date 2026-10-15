# -*- coding: utf-8 -*-
"""Ve so do luong so lieu cho HDSD Bao cao chi phi van chuyen theo NVKD -> hdsd_shots/so_do.png"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'hdsd_shots', 'so_do.png')
F = 'C:/Windows/Fonts/arial.ttf'
FB = 'C:/Windows/Fonts/arialbd.ttf'

W, H = 2000, 1120
im = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(im)
ft = ImageFont.truetype(FB, 38)
fb = ImageFont.truetype(FB, 30)
fs = ImageFont.truetype(F, 24)
f = ImageFont.truetype(F, 24)


def box(x, y, w, h, title, lines, col, fill):
    d.rounded_rectangle((x, y, x + w, y + h), radius=18, outline=col, width=4, fill=fill)
    tw = d.textlength(title, font=fb)
    d.text((x + (w - tw) / 2, y + 18), title, font=fb, fill=col)
    yy = y + 66
    for s in lines:
        sw = d.textlength(s, font=fs)
        d.text((x + (w - sw) / 2, yy), s, font=fs, fill='#374151')
        yy += 32


def arrow(p1, p2, col='#374151', label=None):
    d.line([p1, p2], fill=col, width=4)
    a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 18
    d.polygon([p2, (p2[0] - L * math.cos(a - 0.4), p2[1] - L * math.sin(a - 0.4)),
               (p2[0] - L * math.cos(a + 0.4), p2[1] - L * math.sin(a + 0.4))], fill=col)
    if label:
        for i, t in enumerate(label.split('\n')):
            tw = d.textlength(t, font=f)
            d.text(((p1[0] + p2[0]) / 2 - tw / 2, (p1[1] + p2[1]) / 2 - 64 + i * 28), t, font=f, fill=col)


t = 'Sơ đồ luồng số liệu - Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'
d.text(((W - d.textlength(t, font=ft)) / 2, 30), t, font=ft, fill='#111827')

Y, BW, BH = 170, 410, 250
box(40, Y, BW, BH, 'Yêu cầu xuất hàng', ['Nhân viên kinh doanh lập', 'theo hợp đồng; kho xuất', 'phiếu xuất kho'], '#0EA5E9', '#F0F9FF')
box(530, Y, BW, BH, 'Chuyến xe', ['Điều vận lập chuyến chở hàng', 'cho phiếu xuất kho, hoặc', 'chuyến xe khác'], '#6366F1', '#EEF2FF')
box(1020, Y, BW, BH, 'Phiếu hạch toán', ['Kế toán hạch toán chuyến:', 'mỗi dòng cước gắn 1 nhân', 'viên kinh doanh + mã công việc'], '#F59E0B', '#FFFBEB')
box(1510, Y, 450, BH, 'Báo cáo', ['Phòng ban', '> Nhân viên kinh doanh', '> Từng chuyến (Show chi tiết)'], '#16A34A', '#F0FDF4')
arrow((450, Y + 125), (530, Y + 125))
arrow((940, Y + 125), (1020, Y + 125))
arrow((1430, Y + 125), (1510, Y + 125), '#16A34A')

# khoi khong tinh
box(1020, 540, 940, 250, 'Dòng hạch toán KHÔNG được tính',
    ['- Không gắn nhân viên kinh doanh', '- Mã công việc: Công lái xe, Xăng xe, Chi phí khác,',
     '  Vé cầu đường, Công tác phí', '- Không chọn mã công việc'], '#DC2626', '#FEF2F2')
arrow((1225, Y + BH), (1225, 540), '#DC2626')

# khoi pham vi
box(40, 540, 900, 250, 'Phạm vi xem theo quyền',
    ['Tổng công ty: mọi công ty', 'Công ty: công ty của mình', 'Phòng ban: phòng hiện tại của mình',
     'Không có quyền: chỉ cước gắn chính mình'], '#64748B', '#F8FAFC')
d.line([(490, 540), (490, 480), (1735, 480), (1735, Y + BH)], fill='#64748B', width=3)

# khoi ngay
box(40, 840, 1920, 230, 'Lọc theo thời gian',
    ['Bắt buộc nhập Từ ngày và Đến ngày. Cước được tính theo NGÀY HẠCH TOÁN của phiếu hạch toán.',
     'Số tiền: Chuyến = tổng các dòng của nhân viên trong phiếu; Nhân viên = tổng các chuyến;',
     'Phòng ban = tổng các nhân viên; Tổng cộng = tổng mọi phòng ban ở mọi trang.'], '#0F766E', '#F0FDFA')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print('OK', OUT)
