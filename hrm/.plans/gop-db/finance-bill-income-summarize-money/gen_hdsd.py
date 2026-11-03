# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Tổng hợp tiền về ngân hàng (phân hệ Tài chính / Thông báo) — form chuẩn Danh mục quốc gia (03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Tong hop tien ve ngan hang.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (chạy gen_srs.py trước).
Ảnh: ./thtv_shots (dev-hrm 03/11/2026, script thtv_shots/_capture/capture.js).
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

TEN = 'Tổng hợp tiền về ngân hàng'
SHOTS = os.path.join(HERE, 'thtv_shots')
OUT = os.path.join(HERE, 'HDSD_Tong hop tien ve ngan hang.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_thtv')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu báo có', 'Chứng từ ghi nhận tiền về tài khoản ngân hàng công ty, mã dạng TPE.PBC1026.00052. Màn này hiện các dòng '
                     'tiền về của phiếu báo có đã duyệt.'],
    ['Dòng tiền về', 'Một dòng chi tiết của phiếu báo có (một khoản tiền về). Mỗi dòng của bảng là một dòng tiền về.'],
    ['Số tiền chưa điều chỉnh', 'Số tiền của dòng trừ phần đã điều chỉnh công nợ.'],
    ['Chưa điều chỉnh hết công nợ', 'Dòng còn tiền chưa điều chỉnh (nhãn vàng), tích chọn được để lập phiếu yêu cầu điều chỉnh '
                                    'công nợ.'],
    ['Đã điều chỉnh hết công nợ', 'Dòng đã điều chỉnh hết (nhãn xanh lá), không tích chọn được.'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, xuất Excel, tích chọn dòng, tạo mới điều chỉnh công nợ',
     'Mọi người dùng vào được phân hệ Tài chính hoặc phân hệ Thông báo; chỉ thấy dòng tiền về của công ty mình.'],
    ['Xem chi tiết phiếu báo có (bấm Số báo có)', 'Người tạo phiếu hoặc người có quyền Xem tất cả phiếu báo có của tổng công ty '
                                                 '/ của công ty.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Quản lý tiền ', '@menu_quanlytien',
            ', nhóm Thanh toán tiền mặt ', '@menu_nhom_tttm', ', chọn Tổng hợp tiền về ngân hàng ', '@menu_muc'])
    d.sub(['Hoặc từ phân hệ Thông báo ', '@menu_phanhe_tb', ', tại menu Tra cứu - thông báo ', '@menu_tracuu',
           ', chọn Tổng hợp tiền về ', '@menu_muc_tracuu'])
    d.sub(['Hoặc từ phân hệ Thông báo ', '@menu_phanhe_tb', ', tại menu Thông báo ', '@menu_thongbao',
           ', chọn Tổng hợp tiền về ngân hàng ', '@menu_muc_tb'])
    d.img('01_list', 'Màn hình Tổng hợp tiền về ngân hàng')
    d.step(['Bước 2: Nhập số báo có vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem', ' (hoặc phím Enter)'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai',
            ' để lọc theo Trạng thái (Đã / Chưa điều chỉnh hết công nợ)'])
    for lb, ic in [('Khách hàng (gõ từ 2 ký tự tên, số điện thoại hoặc mã rồi chọn)', 'o_khachhang'),
                   ('Diễn giải (nội dung chuyển khoản)', 'o_diengiai'), ('Ngân hàng (mã hoặc tên)', 'o_nganhang'),
                   ('STK ngân hàng', 'o_stk'), ('Người tạo', 'o_nguoitao'), ('Số tiền (từ → đến)', 'o_sotien'),
                   ('Ngày hạch toán (từ ngày → đến ngày)', 'o_ngayhachtoan')]:
        d.sub(['Hoặc chọn / nhập giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.img('02_filter', 'Khối Bộ lọc danh sách mở Tìm kiếm nâng cao')
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('XEM PHIẾU BÁO CÓ')
    d.step('Bước 1: Truy cập vào màn hình Tổng hợp tiền về ngân hàng (PHẦN 1).')
    d.step(['Bước 2: Bấm vào số báo có ', '@link_ma', '. Hệ thống mở màn “Chi tiết phiếu báo có: <số báo có>”.'])
    d.img('05_detail', 'Màn hình Chi tiết phiếu báo có')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để rời màn chi tiết (về danh sách Phiếu báo có)'])
    d.sub('Hoặc bấm nút Lùi của trình duyệt để về lại màn Tổng hợp tiền về ngân hàng.')

    d.phan('TẠO MỚI ĐIỀU CHỈNH CÔNG NỢ')
    d.step(['Bước 1: Ở cột Điều chỉnh công nợ, tích ', '@chk_dong',
            ' các dòng “Chưa điều chỉnh hết công nợ” của CÙNG một số báo có'])
    d.img('03_select', 'Đã tích 2 dòng của cùng một phiếu báo có')
    d.sub('Tích dòng của phiếu báo có khác: hệ thống báo “Không thể chọn 2 phiếu báo có khác nhau! Vui lòng bỏ chọn dòng cũ '
          'trước.”, bỏ tích dòng cũ rồi chọn lại.')
    d.step(['Bước 2: Bấm ', '@btn_taomoi_dc', '. Hệ thống mở màn “Tạo phiếu yêu cầu điều chỉnh công nợ”.'])
    d.img('04_adjust_create', 'Màn Tạo phiếu yêu cầu điều chỉnh công nợ với các dòng đã chọn')
    d.step('Bước 3: Kiểm tra các trường điền sẵn: Số phiếu báo có, Người tạo, Phòng ban, bảng Điều chỉnh từ (Số tiền = số tiền '
           'chưa điều chỉnh của từng dòng); Loại phiếu chọn sẵn theo phiếu báo có.')
    d.step('Bước 4: Nhập Diễn giải (bắt buộc); ở bảng Điều chỉnh đến chọn Khách hàng, Hợp đồng/Đơn hàng, nhập Số tiền (bắt buộc).')
    d.step('Bước 5: Bấm Lưu nháp hoặc Gửi duyệt. Hệ thống lưu phiếu và quay về màn Tổng hợp tiền về ngân hàng.')
    d.sub(['Hoặc bấm ', '@btn_quaylai_dc', ' để quay về mà không lưu'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ≡ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca_x', ' / ', '@btn_bochonhet_x'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile', '. Hệ thống tải file Tong-hop-tien-ve-ngan-hang.xlsx.'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])

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
