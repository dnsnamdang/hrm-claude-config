# -*- coding: utf-8 -*-
"""Ve so do luong nghiem thu cheo ERP - HRM cho 2 bao cao cong no KH -> so_do_luong.png"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F = 'C:/Windows/Fonts/arial.ttf'
FB = 'C:/Windows/Fonts/arialbd.ttf'
W, H = 2000, 1130
ft = ImageFont.truetype(FB, 38)
fb = ImageFont.truetype(FB, 29)
fs = ImageFont.truetype(F, 23)

im = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(im)


def box(x, y, w, h, title, lines, col, fill):
    d.rounded_rectangle((x, y, x + w, y + h), radius=18, outline=col, width=4, fill=fill)
    tw = d.textlength(title, font=fb)
    d.text((x + (w - tw) / 2, y + 16), title, font=fb, fill=col)
    yy = y + 62
    for s in lines:
        sw = d.textlength(s, font=fs)
        d.text((x + (w - sw) / 2, yy), s, font=fs, fill='#374151')
        yy += 31


def arrow(p1, p2, col='#374151'):
    d.line([p1, p2], fill=col, width=4)
    a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 18
    d.polygon([p2, (p2[0] - L * math.cos(a - 0.4), p2[1] - L * math.sin(a - 0.4)),
               (p2[0] - L * math.cos(a + 0.4), p2[1] - L * math.sin(a + 0.4))], fill=col)


T = 'Luồng nghiệm thu: lập phiếu một lần - kiểm số trên cả ERP và HRM'
d.text(((W - d.textlength(T, font=ft)) / 2, 28), T, font=ft, fill='#111827')

box(40, 120, 600, 250, '1. Chuẩn bị', ['Khách hàng KH-TEST', 'Hợp đồng HD-TEST-01 (nhân viên A lập)',
    'Tài khoản kế toán + tài khoản xem báo cáo', 'Quyền cấp ĐỦ ở cả ERP và HRM', 'Ghi số nền trên 2 hệ thống'],
    '#0F766E', '#F0FDFA')
box(40, 410, 600, 420, '2. Lập phiếu theo luồng', ['Xuất bán hàng (YC xuất > đề nghị xuất kho', '> phiếu xuất kho > phiếu xuất hàng)',
    'Phiếu thu, phiếu báo có', 'Yêu cầu điều chỉnh công nợ > phiếu kế toán', 'Khách trả hàng (YC nhập > ... > phiếu nhập hàng)',
    'Phiếu chi, phiếu ủy nhiệm chi', '', 'Lập ở HRM (màn đã chuyển) hoặc ERP:', 'kết quả như nhau vì dùng chung dữ liệu'],
    '#0EA5E9', '#F0F9FF')
box(760, 330, 460, 300, 'Kế toán hạch toán', ['Ghi vào sổ công nợ phải thu', 'của khách hàng, theo hợp đồng,',
    'theo NGÀY HẠCH TOÁN', '', 'Chưa hạch toán', '= chưa lên báo cáo'], '#6366F1', '#EEF2FF')
box(1340, 120, 620, 300, '3a. Báo cáo trên ERP', ['Kinh doanh > Báo cáo công nợ', '', 'Số chuẩn để so sánh',
    'Có một số lỗi đã biết', '(ghi rõ trong PHẦN 5)'], '#B45309', '#FFFBEB')
box(1340, 540, 620, 300, '3b. Báo cáo trên HRM', ['Bán hàng > Báo cáo > Báo cáo công nợ', '',
    'Phải BẰNG ERP ở mọi ô số', 'trừ các điểm khác đã chốt', '(PHẦN 5)'], '#16A34A', '#F0FDF4')
arrow((340, 370), (340, 410))
arrow((640, 620), (760, 520))
arrow((1220, 440), (1340, 280), '#B45309')
arrow((1220, 520), (1340, 690), '#16A34A')
box(40, 900, 1920, 200, '4. So khớp và ghi kết quả', [
    'Sau MỖI phiếu: chênh lệch so với số nền phải đúng bằng số tiền của phiếu, ở cả ERP và HRM.',
    'Hai hệ thống phải ra cùng một con số ở dòng hợp đồng, dòng khách hàng / nhân viên và dòng Tổng cộng.',
    'Lệch ở điểm đã chốt khác nhau (PHẦN 5): ghi Đạt. Lệch ở chỗ khác: ghi Không đạt, chụp cả 2 màn.',
    'Cuối luồng: kiểm tổng, đổi kỳ, hủy phiếu, phân quyền, xuất Excel, đối chiếu với các báo cáo công nợ khác.'],
    '#7C3AED', '#F5F3FF')
arrow((1650, 840), (1650, 900), '#7C3AED')

out = os.path.join(HERE, 'so_do_luong.png')
im.save(out)
print('OK', out)
