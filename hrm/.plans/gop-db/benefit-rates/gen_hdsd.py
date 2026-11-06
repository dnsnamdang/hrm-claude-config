# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Hệ số công nghệ theo nhóm hàng hóa (màn danh mục, form chuẩn Danh mục quốc gia, 06/11/2026).

Chạy: python gen_hdsd.py  → HDSD_He so cong nghe theo nhom hang hoa.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (hscn_shots/uml/overview.png).
Khuôn cấu trúc: ../bien-ban-xu-ly-thua-thieu-kiem-ke/gen_hdsd.py.
Ảnh + icon: hscn_shots (dev-hrm 06/11/2026, _capture/capture.js chặn mọi yêu cầu ghi). Dev chưa có hệ số nào cho công ty DNS Admin →
danh sách / popup Sửa / Xem / Lịch sử chụp trên DỮ LIỆU GIẢ trả ở trình duyệt (12 hệ số).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Hệ số công nghệ theo nhóm hàng hóa'
SHOTS = os.path.join(HERE, 'hscn_shots')
OUT = os.path.join(HERE, 'HDSD_He so cong nghe theo nhom hang hoa.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_hscn')

THUAT_NGU = [
    ['Hệ số công nghệ (tỷ lệ hưởng công khoán)', 'Hệ số độ khó công nghệ khai cho một hoặc nhiều nhóm hàng hóa; nhân vào công khoán '
                                                'khi duyệt kết quả lắp đặt.'],
    ['Loại tỷ lệ hưởng (Loại hệ số)', 'Tên loại hệ số, không trùng trong cùng công ty.'],
    ['Hệ số', 'Số không âm, tối đa 2 số lẻ.'],
    ['Nhóm hàng hóa áp dụng', 'Các nhóm hàng hóa dùng hệ số này; mỗi nhóm chỉ thuộc một loại hệ số.'],
]
PHIEN_BAN = [['1.0', '06/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Mọi chức năng (Xem, Tạo mới, Sửa, Xóa, Lịch sử, Xuất Excel)', 'Không cần quyền riêng — mọi người dùng đã đăng nhập.'],
    ['Phạm vi dữ liệu', 'Chỉ hệ số thuộc công ty của người đăng nhập.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe', ', tại menu Quy chế - Thiết lập ', '@menu_nhom', ', nhóm Thiết lập ',
            '@menu_nhom2', ', chọn Hệ số công nghệ theo nhóm hàng hóa ', '@menu_muc'])
    d.img('01_list', 'Màn hình Hệ số công nghệ theo nhóm hàng hóa')
    d.step(['Bước 2: Nhập loại hệ số vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_congty', ' để lọc theo Công ty'])
    d.sub(['Hoặc chọn giá trị ', '@o_nguoitao', ' để lọc theo Người tạo'])
    d.sub(['Hoặc chọn giá trị ', '@o_nguoicapnhat', ' để lọc theo Người cập nhật'])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('THÊM MỚI HỆ SỐ')
    d.step('Bước 1: Truy cập vào màn hình Hệ số công nghệ theo nhóm hàng hóa (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi', '. Hệ thống mở cửa sổ “Thêm mới tỷ lệ hưởng công khoán”.'])
    d.img('10_create', 'Cửa sổ Thêm mới tỷ lệ hưởng công khoán')
    d.step(['Bước 3: Nhập đầy đủ thông tin bắt buộc: Loại tỷ lệ hưởng ', '@o_loai', ', Hệ số ', '@o_heso',
            ', chọn một hoặc nhiều Nhóm hàng hóa áp dụng ', '@o_nhom'])
    d.step(['Bước 4: Bấm ', '@btn_luu', ' để lưu và đóng cửa sổ'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu và nhập tiếp hệ số khác'])
    d.sub(['Hoặc ', '@btn_dong', ' để không lưu, chọn ', '@btn_thoat', ' để đóng hoặc ', '@btn_olai', ' để ở lại'])

    d.phan('CHỈNH SỬA HỆ SỐ')
    d.step('Bước 1: Truy cập vào màn hình Hệ số công nghệ theo nhóm hàng hóa.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động'])
    d.step('Bước 3: Hệ thống hiển thị cửa sổ “Chỉnh sửa tỷ lệ hưởng công khoán”.')
    d.img('12_edit', 'Cửa sổ Chỉnh sửa tỷ lệ hưởng công khoán')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Thêm mới).')
    d.step(['Bước 5: Bấm ', '@btn_luu'])
    d.sub(['Hoặc ', '@btn_dong', ' để không lưu'])

    d.xoa('Xác nhận xóa', doi_tuong='hệ số')

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ cửa sổ Xem:')
    d.step(['Bước 1: Bấm vào Loại hệ số ', '@link_ten', ' để mở cửa sổ Xem'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Hệ số công nghệ theo nhóm hàng hóa.')
    d.step(['Bước 2: Bấm vào Loại hệ số ', '@link_ten', '. Hệ thống mở cửa sổ “Xem tỷ lệ hưởng công khoán”.'])
    d.img('17_detail', 'Cửa sổ Xem tỷ lệ hưởng công khoán')
    d.step(['Bước 3: Bấm ', '@btn_dong_view', ' để đóng cửa sổ.'])

    d.xuat_excel(cua_so='Chọn trường xuất file')
    d.tuy_chinh_cot()
    d.cai_dat_bo_loc()
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
