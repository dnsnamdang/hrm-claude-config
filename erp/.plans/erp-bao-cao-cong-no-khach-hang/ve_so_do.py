# -*- coding: utf-8 -*-
"""Ve so do luong so lieu cho HDSD 2 bao cao cong no -> hdsd_shots/so_do_doi_chieu.png, so_do_theo_nv.png"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'hdsd_shots')
F = 'C:/Windows/Fonts/arial.ttf'
FB = 'C:/Windows/Fonts/arialbd.ttf'
W, H = 2000, 1180
ft = ImageFont.truetype(FB, 38)
fb = ImageFont.truetype(FB, 30)
fs = ImageFont.truetype(F, 24)


def ve(out, tieu_de, khoi_bc, khoi_rieng, khoi_cuoi):
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)

    def box(x, y, w, h, title, lines, col, fill):
        d.rounded_rectangle((x, y, x + w, y + h), radius=18, outline=col, width=4, fill=fill)
        tw = d.textlength(title, font=fb)
        d.text((x + (w - tw) / 2, y + 18), title, font=fb, fill=col)
        yy = y + 66
        for s in lines:
            sw = d.textlength(s, font=fs)
            d.text((x + (w - sw) / 2, yy), s, font=fs, fill='#374151')
            yy += 32

    def arrow(p1, p2, col='#374151'):
        d.line([p1, p2], fill=col, width=4)
        a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        L = 18
        d.polygon([p2, (p2[0] - L * math.cos(a - 0.4), p2[1] - L * math.sin(a - 0.4)),
                   (p2[0] - L * math.cos(a + 0.4), p2[1] - L * math.sin(a + 0.4))], fill=col)

    d.text(((W - d.textlength(tieu_de, font=ft)) / 2, 30), tieu_de, font=ft, fill='#111827')
    Y, BH = 150, 330
    box(40, Y, 560, BH, 'Phiếu làm TĂNG nợ', ['Phiếu xuất kho bán hàng', 'Phiếu xuất bán hàng mượn',
        'Phiếu hạch toán dịch vụ / BH-SC', 'Biên bản thanh lý', 'Điều chỉnh công nợ tăng',
        'Phiếu chi, ủy nhiệm chi trả lại tiền'], '#0EA5E9', '#F0F9FF')
    box(40, Y + BH + 40, 560, 290, 'Phiếu làm GIẢM nợ', ['Phiếu thu, phiếu báo có',
        'Phiếu nhập hàng khách trả lại', 'Điều chỉnh công nợ giảm', 'Khai báo đầu kỳ (phần đã thu)'],
        '#F59E0B', '#FFFBEB')
    box(720, Y + 150, 460, 330, 'Hạch toán', ['Kế toán hạch toán phiếu:', 'ghi vào công nợ phải thu',
        'của khách hàng, theo', 'hợp đồng, theo ngày hạch toán', '', 'Phiếu chưa hạch toán', '= chưa lên báo cáo'],
        '#6366F1', '#EEF2FF')
    box(1300, Y, 660, 480, khoi_bc[0], khoi_bc[1], '#16A34A', '#F0FDF4')
    arrow((600, Y + 165), (720, Y + 260))
    arrow((600, Y + BH + 185), (720, Y + 400))
    arrow((1180, Y + 315), (1300, Y + 315), '#16A34A')
    box(1300, Y + 520, 660, 240, khoi_rieng[0], khoi_rieng[1], '#DC2626', '#FEF2F2')
    box(40, 970, 1920, 180, 'Cách tính số dư', khoi_cuoi, '#0F766E', '#F0FDFA')
    os.makedirs(SHOTS, exist_ok=True)
    im.save(out)
    print('OK', out)


CUOI = ['Số dư đầu kỳ = phát sinh có ngày hạch toán TRƯỚC Từ ngày.',
        'Số dư cuối kỳ = Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Số dương: khách còn nợ; số âm: khách trả thừa.']

ve(os.path.join(SHOTS, 'so_do_doi_chieu.png'),
   'Sơ đồ luồng số liệu - Bảng đối chiếu công nợ 1 khách hàng',
   ('Bảng đối chiếu', ['Chọn kỳ + khách hàng (bắt buộc)', '', 'Dòng Tổng cộng', '> Dòng hợp đồng (chữ đậm)',
                       '> Từng chứng từ theo ngày', '   (số dư chạy sau mỗi chứng từ)', '', 'In / Xuất Excel để gửi',
                       'khách xác nhận công nợ']),
   ('Lưu ý khi đối chiếu', ['Dòng hợp đồng: Số dư đầu kỳ để trống,', 'số dư không tính 2 cột Điều chỉnh công nợ.',
                            'Dòng Tổng cộng: tính đủ mọi cột', 'và cả phát sinh không gắn hợp đồng.']),
   CUOI)

ve(os.path.join(SHOTS, 'so_do_theo_nv.png'),
   'Sơ đồ luồng số liệu - Báo cáo tổng hợp công nợ khách hàng theo nhân viên',
   ('Báo cáo theo nhân viên', ['Chọn kỳ (bắt buộc)', '', 'Dòng Tổng cộng', '> Nhân viên lập hợp đồng (chữ đậm)',
                               '> Từng hợp đồng + khách hàng', '', 'Ngày nghiệm thu, Số ngày nợ', 'để giao nhân viên đi thu nợ']),
   ('Phạm vi xem theo quyền', ['Tổng công ty / Công ty / Phòng ban / Bộ phận', '(gồm cả hợp đồng mình lập)',
                               'Không có quyền: chỉ hợp đồng mình lập']),
   CUOI)
