# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Khai báo hạn mức công nợ KH (danh sách khách → dòng theo công ty, sửa thẳng trong bảng + Lưu từng khách), 18/11/2026.

Chạy: python gen_hdsd.py  → HDSD_Khai bao han muc cong no KH.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (kbhmcn_shots/uml/overview.png).
Khuôn cấu trúc: ../benefit-rates/gen_hdsd.py.
Ảnh + icon: kbhmcn_shots (dev-hrm 18/11/2026, _capture/capture.js chặn mọi yêu cầu ghi — 0 yêu cầu ghi; KHÔNG bấm Lưu).
Thứ tự phần theo skill: Truy cập & tìm kiếm → Khai báo / chỉnh sửa → Lịch sử → Xuất Excel → Tùy chỉnh cột. Màn không có Thêm mới /
Xóa / Khóa / Xem chi tiết / Import / Cài đặt bộ lọc (bộ lọc chỉ 2 ô nên hiện thẳng).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Khai báo hạn mức công nợ KH'
SHOTS = os.path.join(HERE, 'kbhmcn_shots')
OUT = os.path.join(HERE, 'HDSD_Khai bao han muc cong no KH.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_kbhmcn')

THUAT_NGU = [
    ['Dòng công ty (dòng hạn mức)', 'Hạn mức khai cho một khách tại một công ty (cột Khai báo theo công ty).'],
    ['Cách tính lãi', 'Theo vượt hạn mức công nợ hoặc Theo thời gian thanh toán.'],
    ['Hạn mức công nợ tính lãi', 'Số tiền nguyên, tối đa 999,999,999,999,999; có nhập thì phải chọn Cách tính lãi.'],
    ['Hạn mức công nợ xuất hàng', 'Số tiền nguyên, tối đa 999,999,999,999,999; ngưỡng kiểm vượt hạn mức khi gửi duyệt phiếu xuất.'],
]
PHIEN_BAN = [['1.0', '18/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, lịch sử, xuất Excel, tùy chỉnh cột', 'Không cần quyền — mọi người dùng đã đăng nhập.'],
    ['Khai báo / sửa hạn mức (dòng công ty mình)', 'Quản lý khai báo hạn mức công nợ khách hàng.'],
    ['Thấy dòng của mọi công ty khi có quyền Quản lý', 'Xem khai báo hạn mức công nợ khách hàng (thiếu quyền này thì người có quyền '
                                                       'Quản lý chỉ thấy dòng công ty mình).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kế toán công nợ ', '@menu_ketoancongno', ', nhóm Khách hàng ',
            '@menu_nhom_kh', ', chọn Khai báo hạn mức công nợ KH ', '@menu_muc'])
    d.img('01_list', 'Màn hình Khai báo hạn mức công nợ khách hàng')
    d.step(['Bước 2: Nhập số điện thoại, mã số thuế hoặc CMND của khách vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Gõ ít nhất 2 ký tự mã hoặc tên khách vào ô ', '@o_khachhang', ' rồi chọn khách để lọc'])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('KHAI BÁO / CHỈNH SỬA HẠN MỨC')
    d.step('Bước 1: Truy cập vào màn hình Khai báo hạn mức công nợ KH và tìm khách cần khai (PHẦN 1). Dòng có tên công ty của bạn '
           'trong cột Khai báo theo công ty hiện ô nhập.')
    d.img('10_edit', 'Dòng công ty của bạn có ô nhập trên bảng')
    d.step(['Bước 2: Chọn Cách tính lãi ', '@o_cachtinhlai'])
    d.step(['Bước 3: Nhập Hạn mức công nợ tính lãi ', '@o_hanmuc_lai', ' (đã nhập thì bắt buộc chọn Cách tính lãi)'])
    d.step(['Bước 4: Nhập Hạn mức công nợ xuất hàng ', '@o_hanmuc_xuat'])
    d.step(['Bước 5: Bấm ', '@btn_luu_row', ' ở cột Hành động của khách đó để lưu'])
    d.sub(['Hoặc rời màn khi chưa lưu, chọn ', '@btn_thoat', ' ở hộp “Thông tin chưa lưu” để bỏ thay đổi hoặc ', '@btn_olai',
           ' để ở lại'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.step(['Bước 1: Ở cột Hành động của khách, bấm ', '@btn_lichsu_row'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi')
    d.step(['Bước 2: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 3: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

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
