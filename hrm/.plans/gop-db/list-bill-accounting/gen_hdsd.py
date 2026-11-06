# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Danh sách loại phiếu hạch toán (màn danh mục CHỈ XEM, form chuẩn Danh mục quốc gia, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Danh sach loai phieu hach toan.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (dslpht_shots/uml/overview.png).
Khuôn cấu trúc: ../benefit-rates/gen_hdsd.py. Màn không có Thêm / Sửa / Xóa / Lịch sử / Xem chi tiết / Cài đặt bộ lọc (bộ lọc gọn 2 ô)
→ HDSD chỉ có: Truy cập và tìm kiếm, Sắp xếp và phân trang, Xuất Excel, Tùy chỉnh cột.
Ảnh + icon: dslpht_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi — 0 yêu cầu; dữ liệu thật 105 loại phiếu).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Danh sách loại phiếu hạch toán'
SHOTS = os.path.join(HERE, 'dslpht_shots')
OUT = os.path.join(HERE, 'HDSD_Danh sach loai phieu hach toan.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_dslpht')

THUAT_NGU = [
    ['Loại phiếu hạch toán', 'Tên chuẩn của một loại phiếu trong hệ thống (vd “PXH - Xuất bán hàng”, “PC - Chi trả nhà cung cấp”).'],
    ['Phân loại', 'Nhóm lớn của loại phiếu: Đề nghị xuất, Đề nghị nhập, Xuất hàng, Nhập hàng, Thu, Chi, Phiếu kế toán, Dịch vụ, Khác.'],
    ['Hạch toán riêng', 'Loại phiếu được hạch toán riêng thì cột có dấu ✓, không thì để trống.'],
    ['PXH / PNH / PT / PC', 'Phiếu xuất hàng / Phiếu nhập hàng / Phiếu thu / Phiếu chi.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (Xem, Tìm kiếm, Xuất Excel, Tùy chỉnh cột)', 'Không cần quyền riêng — mọi người dùng đã đăng nhập.'],
    ['Phạm vi dữ liệu', 'Toàn bộ 105 loại phiếu của hệ thống (không giới hạn theo công ty).'],
    ['Thêm, Sửa, Xóa', 'Màn chỉ dùng để tra cứu, không có các chức năng này.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe', ', tại menu Quy chế - Thiết lập ', '@menu_nhom', ', nhóm Thiết lập ',
            '@menu_nhom2', ', chọn Danh sách loại phiếu hạch toán ', '@menu_muc'])
    d.img('01_list', 'Màn hình Danh sách loại phiếu hạch toán')
    d.step(['Bước 2: Nhập tên loại phiếu (hoặc một phần tên, vd “Xuất thẳng”) vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem', ' (hoặc phím Enter)'])
    d.step(['Bước 4: Chọn giá trị trong ', '@o_phanloai', ' để lọc theo Phân loại — danh sách lọc ngay khi chọn'])
    d.img('02b_filter_full', 'Kết quả tìm “PT” với Phân loại = Thu')
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('SẮP XẾP VÀ PHÂN TRANG')
    d.step('Bước 1: Truy cập vào màn hình Danh sách loại phiếu hạch toán (PHẦN 1).')
    d.step('Bước 2: Bấm tiêu đề cột Loại phiếu hoặc Phân loại để sắp xếp tăng dần; bấm lần nữa để sắp xếp giảm dần.')
    d.img('03_sort', 'Danh sách sắp xếp giảm dần theo Phân loại')
    d.step('Bước 3: Ở cuối bảng, chọn Số dòng/trang (5, 10, 20, 50, 100) hoặc bấm số trang, « ‹ › » để xem trang khác.')

    d.xuat_excel(cua_so='Chọn trường xuất file')
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
