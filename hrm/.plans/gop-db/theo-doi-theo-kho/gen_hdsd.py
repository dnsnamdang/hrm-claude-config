# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Theo dõi theo kho (phân hệ Kho, mục cấp 1, 2 trang), form chuẩn, 10/11/2026.

Chạy: python gen_hdsd.py  → HDSD_Theo doi theo kho.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Khuôn: ../hoat-dong-kho/gen_hdsd.py (10/11, cùng bảng hoạt động).
Màn chỉ đọc: không Thêm / Sửa / Xóa / Lịch sử / In / Cài đặt bộ lọc → HDSD có: Truy cập và tìm kiếm, Sắp xếp và phân trang, Xem hoạt
động nhập/xuất của kho, Mở phiếu đề nghị, Xuất Excel, Tùy chỉnh cột.
Ảnh + icon: tdtk_shots (dev-hrm 10/11/2026, DNS Admin, dữ liệu thật; _capture/capture.js chặn mọi yêu cầu ghi — 0).
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

TEN = 'Theo dõi theo kho'
SHOTS = os.path.join(HERE, 'tdtk_shots')
OUT = os.path.join(HERE, 'HDSD_Theo doi theo kho.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_tdtk')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Kho', 'Kho vật lý khai ở danh mục Kho vật lý (mã, tên, nhóm, công ty).'],
    ['Phiếu đề nghị xuất kho / nhập kho', 'Phiếu yêu cầu thủ kho xuất hàng (mã PDNXK-…) / nhận hàng vào kho (mã PDNNK-…).'],
    ['Đã nhận đề nghị', 'Phiếu đã gửi tới thủ kho, chưa bắt đầu lấy / xếp hàng.'],
    ['Đang lấy hàng / Đang xếp hàng', 'Thủ kho đã lập phiếu xuất kho / phiếu nhập kho, hàng chưa xong.'],
    ['Đã hoàn thành', 'Hàng đã xuất / nhập kho xong; phiếu còn trên bảng tới hết ngày nhận.'],
    ['Tổng thời gian xử lý', 'Từ Thời gian nhận tới Thời gian hoàn thành.'],
]
PHIEN_BAN = [['1.0', '10/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (xem danh sách kho, xem hoạt động của kho, tìm kiếm, mở phiếu, xuất Excel, tùy chỉnh cột)', 'Quản lý kho'],
    ['Xem kho của mọi công ty, lọc theo Công ty', 'Xem danh mục kho của tất cả công ty (không có quyền này thì chỉ thấy kho công ty mình)'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap([('Kho', 'menu_phanhe'), ('Theo dõi theo kho', 'menu_muc')], 'mã hoặc tên kho (một phần, vd “phan”)',
               bo_loc=[('Nhóm', 'o_nhom'), ('Công ty (chỉ hiện khi bạn được xem mọi công ty)', 'o_congty')], nang_cao=False)
    d.sub(['Hoặc bấm ', '@btn_x_timnhanh', ' trong ô tìm kiếm để xóa chữ đã nhập'])

    d.phan('SẮP XẾP VÀ PHÂN TRANG')
    d.step('Bước 1: Truy cập vào màn hình Theo dõi theo kho (PHẦN 1).')
    d.step(['Bước 2: Bấm tiêu đề cột Mã hoặc Tên có biểu tượng ', '@o_sort', ' để sắp tăng dần; bấm lần nữa để giảm dần'])
    d.img('03_sort', 'Danh sách kho sắp xếp theo cột Mã')
    d.step(['Bước 3: Chọn số dòng mỗi trang ở ô ', '@o_sodong'])
    d.step(['Bước 4: Bấm số trang hoặc mũi tên ở thanh ', '@o_phantrang', ' để chuyển trang'])

    d.phan('XEM HOẠT ĐỘNG NHẬP/XUẤT CỦA KHO')
    d.step('Bước 1: Truy cập vào màn hình Theo dõi theo kho (PHẦN 1), tìm kho cần xem.')
    d.step(['Bước 2: Bấm mã kho ', '@link_makho', ' (hoặc tên kho). Hệ thống mở trang “Hoạt động nhập/xuất kho <mã> - <tên>” ở tab mới.'])
    d.img('10_detail', 'Trang hoạt động nhập/xuất của kho PTT')
    d.step(['Bước 3: Rê chuột vào ', '@ic_info', ' để xem giải thích khối Phiếu nhận và từng ô tổng hợp'])
    d.step(['Bước 4: Nhập mã phiếu (hoặc một phần mã, vd “PDNNK”) vào ô ', '@o_timphieu', ', nhấn ', '@btn_timkiem'])
    d.sub(['Hoặc bấm ', '@btn_lammoi', ' để xóa giá trị đã tìm'])
    d.step(['Bước 5: Bấm tiêu đề cột có biểu tượng ', '@o_sort_act',
            ' (Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành) để sắp xếp'])
    d.step(['Bước 6: Bấm ', '@btn_thugon', ' để ẩn 3 ô tổng hợp'])
    d.sub(['Hoặc bấm ', '@btn_morong', ' để hiện lại'])
    d.step('Bước 7: Để trang mở, bảng và các ô tổng hợp tự cập nhật mỗi 60 giây.')
    d.step(['Bước 8: Bấm ', '@btn_quaylai', ' để về danh sách kho (bộ lọc vừa dùng vẫn còn)'])

    d.phan('MỞ PHIẾU ĐỀ NGHỊ')
    d.step('Bước 1: Mở trang hoạt động nhập/xuất của kho (PHẦN 3).')
    d.step(['Bước 2: Bấm mã phiếu ', '@link_maphieu', ' ở cột Phiếu đề nghị. Hệ thống mở màn chi tiết phiếu ở tab mới.'])
    d.img('15_dnxk', 'Màn chi tiết Phiếu đề nghị xuất kho')
    d.step('Bước 3: Xem / xử lý phiếu ở tab mới, rồi quay lại tab hoạt động để theo dõi.')

    d.xuat_excel(cua_so='Chọn trường xuất Excel')
    d.p('Ở trang hoạt động của kho, bấm Xuất Excel và làm tương tự để xuất bảng phiếu của kho đó:')
    d.img('21_export_act', 'Cửa sổ Chọn trường xuất Excel ở trang hoạt động của kho')
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
