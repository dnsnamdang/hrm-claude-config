# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Báo cáo hạn mức công nợ khách hàng (phân hệ Tài chính) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Bao cao han muc cong no khach hang.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Ảnh: ./bchmcn_shots (dev-hrm 03/11/2026, DNS Admin, script bchmcn_shots/_capture/capture.js).
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

TEN = 'Báo cáo hạn mức công nợ khách hàng'
SHOTS = os.path.join(HERE, 'bchmcn_shots')
OUT = os.path.join(HERE, 'HDSD_Bao cao han muc cong no khach hang.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_bchmcn')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Hạn mức tính lãi', 'Mức dư nợ mà vượt quá sẽ bị tính lãi; khai ở màn Khai báo hạn mức công nợ khách hàng.'],
    ['Hạn mức được nợ', 'Mức dư nợ tối đa còn được xuất hàng (ô “Hạn mức công nợ xuất hàng” ở màn Khai báo).'],
    ['Số dư nợ hiện tại', 'Cột của báo cáo, luôn hiện 0 (giữ y như hệ thống ERP). Công nợ thật xem ở cửa sổ theo NVKD.'],
    ['NVKD', 'Nhân viên kinh doanh — người lập hợp đồng của khoản công nợ.'],
    ['Chỉ tiêu vượt hạn mức', 'Ô lọc 4 giá trị; hiện chỉ “Trong hạn mức tính lãi” ra dữ liệu (khách có hạn mức tính lãi > 0).'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem báo cáo, tìm kiếm, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel, xem chi tiết theo NVKD',
     'Mọi người dùng vào được phân hệ Tài chính; chỉ thấy khách hàng có hạn mức khai cho công ty mình.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Kế toán công nợ ', '@menu_ketoancongno',
            ', nhóm Khách hàng ', '@menu_nhom_kh', ', chọn Báo cáo hạn mức công nợ khách hàng ', '@menu_muc'])
    d.img('01_list', 'Màn hình Báo cáo hạn mức công nợ khách hàng')
    d.step(['Bước 2: Nhập mã hoặc tên khách hàng vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem', ' (hoặc phím Enter)'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_chitieu',
            ' để lọc theo Chỉ tiêu vượt hạn mức (mặc định để trống = tất cả)'])
    d.sub(['Hoặc gõ từ 2 ký tự tên, số điện thoại hoặc mã vào ', '@o_khachhang', ' rồi chọn khách hàng để lọc theo Khách hàng'])
    d.sub(['Hoặc chọn giá trị trong ', '@o_loaihinh', ' để lọc theo Loại hình tổ chức'])
    d.sub(['Hoặc chọn Từ ngày → Đến ngày trong ', '@o_thoigian',
           ' (chọn đủ 2 ngày; dùng làm mốc tính công nợ khi xem chi tiết theo NVKD, không lọc bảng)'])
    d.img('02_filter', 'Khối Bộ lọc danh sách mở Tìm kiếm nâng cao')
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('XEM CHI TIẾT HẠN MỨC DƯ NỢ THEO NVKD')
    d.step('Bước 1: Truy cập vào màn hình Báo cáo hạn mức công nợ khách hàng (PHẦN 1).')
    d.step(['Bước 2: Bấm vào mã khách hàng ', '@link_ma',
            '. Hệ thống mở cửa sổ “Chi tiết hạn mức dư nợ khách hàng <mã> - <tên> theo NVKD”.'])
    d.img('03_popup', 'Cửa sổ Chi tiết hạn mức dư nợ khách hàng theo NVKD')
    d.step(['Bước 3: Chọn nhân viên trong ', '@o_nhanvien', ' để chỉ xem công nợ của nhân viên đó (bỏ trống = tất cả)'])
    d.sub('Hoặc bấm tiêu đề cột Công nợ để sắp xếp tăng dần, bấm lần nữa để sắp giảm dần.')
    d.img('03b_popup_filter', 'Cửa sổ lọc theo một nhân viên')
    d.step(['Bước 4: Bấm ', '@btn_dong_popup', ' để đóng cửa sổ, quay lại báo cáo'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc báo cáo theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ≡ để đổi vị trí các trường cần xuất (mặc định tích các cột đang hiện trên bảng).')
    d.sub(['Hoặc bấm ', '@btn_chontatca_x', ' / ', '@btn_bochonhet_x'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile', '. Hệ thống tải file bao-cao-han-muc-cong-no-khach-hang.xlsx.'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.sub('Báo cáo không có dòng nào: hệ thống báo “Không có dữ liệu để xuất”, không tạo file.')

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
