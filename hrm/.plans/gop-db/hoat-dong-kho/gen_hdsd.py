# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Hoạt động kho (phân hệ Kho, mục cấp 1), form chuẩn, 10/11/2026.

Chạy: python gen_hdsd.py  → HDSD_Hoat dong kho.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Khuôn: ../list-bill-accounting/gen_hdsd.py (màn chỉ xem dạng danh sách) + ../tong-hop-xuat-nhap-ton/gen_hdsd.py (09/11).
Màn chỉ đọc: không Thêm / Sửa / Xóa / Lịch sử / In / Cài đặt bộ lọc → HDSD có: Truy cập và tìm kiếm, Sắp xếp và theo dõi, Mở phiếu đề
nghị, Xuất Excel, Tùy chỉnh cột.
Ảnh + icon: hdk_shots (dev-hrm 10/11/2026, DNS Admin, _capture/capture.js chặn mọi yêu cầu ghi — 0). Ảnh có dữ liệu = dữ liệu thật kho PTT
thay vào trên trình duyệt (DNS Admin không là thủ kho kho nào trên dev) — xem docstring gen_srs.py.
"""
import os
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Hoạt động kho'
SHOTS = os.path.join(HERE, 'hdk_shots')
OUT = os.path.join(HERE, 'HDSD_Hoat dong kho.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_hdk')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu đề nghị xuất kho / nhập kho', 'Phiếu yêu cầu thủ kho xuất hàng (mã PDNXK-…) / nhận hàng vào kho (mã PDNNK-…).'],
    ['Thủ kho', 'Người được gán ở ô Thủ kho của kho trong danh mục Kho vật lý; màn chỉ hiện phiếu của các kho bạn là thủ kho.'],
    ['Đã nhận đề nghị', 'Phiếu đã gửi tới thủ kho, chưa bắt đầu lấy / xếp hàng.'],
    ['Đang lấy hàng / Đang xếp hàng', 'Thủ kho đã lập phiếu xuất kho / phiếu nhập kho, hàng chưa xong.'],
    ['Đã hoàn thành', 'Hàng đã xuất / nhập kho xong; phiếu còn trên bảng tới hết ngày nhận.'],
    ['Tổng thời gian xử lý', 'Từ Thời gian nhận tới Thời gian hoàn thành.'],
]
PHIEN_BAN = [['1.0', '10/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (xem, tìm kiếm, mở phiếu, xuất Excel, tùy chỉnh cột)', 'Không cần quyền riêng — mọi người dùng đã đăng nhập.'],
    ['Phạm vi dữ liệu', 'Phiếu của các kho bạn là Thủ kho; không là thủ kho kho nào thì danh sách trống.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Kho ', '@menu_phanhe', ', chọn ', '@menu_muc'])
    d.img('01_list', 'Màn hình Hoạt động kho')
    d.step(['Bước 2: Nhập mã phiếu (hoặc một phần mã, vd “39053”) vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem', ' (hoặc phím Enter)'])
    d.sub(['Hoặc bấm ', '@btn_x_timnhanh', ' trong ô để xóa chữ đã nhập'])
    d.step(['Bước 4: Chọn ', '@btn_lammoi', ' để xóa giá trị đã tìm'])

    d.phan('SẮP XẾP VÀ THEO DÕI')
    d.step('Bước 1: Truy cập vào màn hình Hoạt động kho (PHẦN 1).')
    d.step(['Bước 2: Bấm tiêu đề cột có biểu tượng sắp xếp ', '@o_sort',
            ' (Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành) để sắp tăng dần; bấm lần nữa để giảm dần'])
    d.img('03_sort', 'Danh sách sắp xếp theo cột Phiếu đề nghị')
    d.step(['Bước 3: Rê chuột vào ', '@ic_info', ' để xem giải thích khối Phiếu nhận và từng ô tổng hợp'])
    d.step(['Bước 4: Bấm ', '@btn_thugon', ' để ẩn 3 ô tổng hợp'])
    d.sub(['Hoặc bấm ', '@btn_morong', ' để hiện lại'])
    d.step('Bước 5: Để màn hình mở, danh sách và các ô tổng hợp tự cập nhật mỗi 60 giây.')

    d.phan('MỞ PHIẾU ĐỀ NGHỊ')
    d.step('Bước 1: Truy cập vào màn hình Hoạt động kho (PHẦN 1).')
    d.step(['Bước 2: Bấm mã phiếu ', '@link_maphieu', ' ở cột Phiếu đề nghị. Hệ thống mở màn chi tiết phiếu ở tab mới.'])
    d.img('05_dnxk', 'Màn chi tiết Phiếu đề nghị xuất kho')
    d.step('Bước 3: Xử lý phiếu ở tab mới, rồi quay lại tab Hoạt động kho để theo dõi.')

    d.xuat_excel(cua_so='Chọn trường xuất Excel')
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    os.makedirs(CHECK_DIR, exist_ok=True)
    pdf = os.path.join(CHECK_DIR, 'HDSD.pdf')
    size = finalize_word(out, pdf)
    print('docx', out, size)
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(CHECK_DIR, 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
