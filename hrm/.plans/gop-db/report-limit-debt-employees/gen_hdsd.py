# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Báo cáo hạn mức công nợ nhân viên (phân hệ Tài chính) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Bao cao han muc cong no nhan vien.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Ảnh: ./bchmcnnv_shots (dev-hrm 03/11/2026, DNS Admin, script bchmcnnv_shots/_capture/capture.js).
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

TEN = 'Báo cáo hạn mức công nợ nhân viên'
SHOTS = os.path.join(HERE, 'bchmcnnv_shots')
OUT = os.path.join(HERE, 'HDSD_Bao cao han muc cong no nhan vien.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_bchmcnnv')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Hạn mức công nợ xuất hàng', 'Mức công nợ khách hàng tối đa nhân viên được để tồn khi xuất hàng; khai ở form Tài khoản nhân viên '
                                  '(Quản trị hệ thống › Người dùng & phân quyền).'],
    ['Tổng công nợ khách hàng hiện tại', 'Công nợ khách hàng thuộc các hợp đồng do nhân viên tạo, tính như hệ thống ERP tới “Đến ngày” '
                                         'của bộ lọc (trống = hôm nay).'],
    ['Chỉ tiêu vượt hạn mức', 'Ô lọc 2 giá trị: Trong hạn mức (công nợ nhỏ hơn hạn mức), Vượt hạn mức (công nợ lớn hơn hạn mức).'],
    ['Công nợ theo khách hàng', 'Số trong cửa sổ chi tiết, cộng dồn qua các khách hàng giống hệ thống ERP (không phải nợ riêng từng '
                                'khách).'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem báo cáo, tìm kiếm, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel, xem chi tiết theo khách hàng',
     'Mọi người dùng vào được phân hệ Tài chính; xem được nhân viên của mọi công ty.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kế toán công nợ ', '@menu_ketoancongno',
            ', nhóm Nhân viên ', '@menu_nhom_nv', ', chọn Báo cáo hạn mức công nợ nhân viên ', '@menu_muc'])
    d.img('01_list', 'Màn hình Báo cáo hạn mức công nợ nhân viên')
    d.step(['Bước 2: Nhập mã hoặc tên nhân viên vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem', ' (hoặc phím Enter)'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_chitieu',
            ' để lọc theo Chỉ tiêu vượt hạn mức (mặc định để trống = tất cả)'])
    d.sub(['Hoặc chọn ', '@o_congty', ', ', '@o_phongban', ', ', '@o_bophan',
           ' để lọc theo đơn vị (chọn cấp trên thì cấp dưới tự xóa)'])
    d.sub(['Hoặc gõ tên vào ', '@o_nhanvien', ' rồi chọn nhân viên để xem riêng nhân viên đó'])
    d.sub(['Hoặc chọn Từ ngày → Đến ngày trong ', '@o_thoigian',
           ' (chọn đủ 2 ngày; công nợ tính tới Đến ngày)'])
    d.img('02_filter', 'Khối Bộ lọc danh sách mở Tìm kiếm nâng cao')
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])
    d.step(['Bước 6: Rê chuột vào biểu tượng ', '@icon_info', ' ở đầu cột để xem cách tính của cột'])
    d.img('01b_tip', 'Giải thích cột Tổng công nợ khách hàng hiện tại')

    d.phan('XEM CHI TIẾT HẠN MỨC DƯ NỢ THEO KHÁCH HÀNG')
    d.step('Bước 1: Truy cập vào màn hình Báo cáo hạn mức công nợ nhân viên (PHẦN 1).')
    d.step(['Bước 2: Bấm vào mã nhân viên ', '@link_ma',
            '. Hệ thống mở cửa sổ “Thông tin chi tiết hạn mức dư nợ nhân viên <mã> - <tên> theo khách hàng”.'])
    d.img('03_popup', 'Cửa sổ Thông tin chi tiết hạn mức dư nợ nhân viên theo khách hàng')
    d.step(['Bước 3: Nhập mã hoặc tên khách hàng vào ', '@o_timnhanh_pop', ', bấm ', '@btn_timkiem'])
    d.sub(['Hoặc chọn khách hàng trong ', '@o_khachhang_pop', ' (lọc ngay khi chọn)'])
    d.sub(['Hoặc nhập khoảng công nợ vào ', '@o_sotien', ', bấm ', '@btn_timkiem'])
    d.sub('Hoặc bấm tiêu đề cột Công nợ để sắp xếp tăng dần, bấm lần nữa để sắp giảm dần.')
    d.step(['Bước 4: Bấm ', '@btn_lammoi', ' để xóa giá trị đã lọc trong cửa sổ'])
    d.step(['Bước 5: Bấm ', '@btn_dong_popup', ' để đóng cửa sổ, quay lại báo cáo'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ≡ để đổi vị trí các trường cần xuất (mặc định tích các cột đang hiện trên bảng).')
    d.sub(['Hoặc bấm ', '@btn_chontatca_x', ' / ', '@btn_bochonhet_x'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile', '. Hệ thống tải file bao-cao-han-muc-cong-no-nhan-vien.xlsx.'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.sub('Báo cáo không có dòng nào: hệ thống vẫn tải file có tiêu đề và tên cột, phần dữ liệu để trống.')

    d.cai_dat_bo_loc()
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
