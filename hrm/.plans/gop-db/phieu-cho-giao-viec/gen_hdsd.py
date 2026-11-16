# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu chờ giao việc (form chuẩn Danh mục quốc gia, 12/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu cho giao viec.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra (pcgv_shots/uml/overview.png).
Khuôn cấu trúc: ../bien-ban-ban-giao-nghiem-thu/gen_hdsd.py. PHẦN 1 viết tay (thêm bước chọn tab giữa Bước 1 và ô tìm nhanh).
Ảnh + icon: pcgv_shots (dev-hrm 12/11/2026, _capture/capture.js, chặn mọi yêu cầu ghi — 0 yêu cầu ghi). Ảnh có nút Tạo phiếu giao việc /
Từ chối tiếp nhận ở tab Hợp đồng, PL bổ sung, Lắp đặt là GIẢ cờ trên trình duyệt (DNS Admin không thuộc phòng tiếp nhận nào).
btn_luu.png = bản sao btn_luu_cfg.png (hàm chung cai_dat_bo_loc() đọc tên btn_luu).
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu chờ giao việc'
SHOTS = os.path.join(HERE, 'pcgv_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu cho giao viec.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_pcgv')

THUAT_NGU = [
    ['Phiếu chờ giao việc', 'Danh sách các chứng từ còn công việc / dịch vụ / hàng chưa giao việc, chia 5 thẻ: Hợp đồng, PL bổ sung, '
                            'Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác.'],
    ['Phòng tiếp nhận xử lý', 'Phòng được chỉ định lập phiếu giao việc cho chứng từ.'],
    ['Phiếu giao việc', 'Chứng từ giao việc cho kỹ thuật, lập bằng nút Tạo phiếu giao việc.'],
    ['Có hiệu lực', 'Trạng thái (nhãn xanh dương) của hợp đồng / PL bổ sung đang chờ giao việc.'],
    ['Đã duyệt', 'Trạng thái (nhãn xanh lá) của phiếu bảo hành đang chờ giao việc.'],
    ['Chờ giao việc', 'Trạng thái (nhãn cam) của phiếu yêu cầu lắp đặt / yêu cầu giao việc khác.'],
]
PHIEN_BAN = [['1.0', '12/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, tìm kiếm, xuất Excel, in', 'Không cần quyền riêng. Thẻ Hợp đồng, PL bổ sung, Lắp đặt bàn giao: chỉ chứng từ của '
                                               'phòng mình quản lý; có quyền Xem danh sách phiếu chờ giao việc (mức Tổng công ty) '
                                               'thì xem tất cả.'],
    ['Tạo phiếu giao việc, Từ chối tiếp nhận xử lý', 'Tạo phiếu giao việc và thuộc phòng tiếp nhận xử lý của chứng từ.'],
    ['Đóng hợp đồng', 'Người lập hoặc người quản lý phòng của hợp đồng.'],
    ['Hủy duyệt hợp đồng', 'Người quản lý phòng của hợp đồng.'],
    ['Quyết toán hợp đồng', 'Người lập hợp đồng.'],
]
TABS = [('Hợp đồng', 'tab_contract'), ('PL bổ sung', 'tab_addition_annex'), ('Phiếu bảo hành', 'tab_warranty'),
        ('Lắp đặt bàn giao', 'tab_assembly'), ('Giao việc khác', 'tab_other')]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.step(['Bước 1: Từ phân hệ CSKH sau bán ', '@menu_phanhe', ', tại menu Giao việc ', '@menu_nhom',
            ', chọn Phiếu chờ giao việc ', '@menu_muc'])
    d.img('01_list', 'Màn hình Phiếu chờ giao việc')
    d.step(['Bước 2: Chọn thẻ ', '@' + TABS[0][1], ' để xem hợp đồng chờ giao việc'])
    for lb, ic in TABS[1:]:
        d.sub(['Hoặc chọn thẻ ', '@' + ic, ' để xem %s' % lb])
    d.step(['Bước 3: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 4: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 5: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_nguoiduyet', ' để lọc theo Người duyệt hợp đồng'])
    for lb, ic in [('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'), ('Khách hàng', 'o_khachhang'),
                   ('Hàng hóa (thẻ Phiếu bảo hành)', 'o_hanghoa'), ('Số hợp đồng (thẻ Lắp đặt, Giao việc khác)', 'o_sohd'),
                   ('Ngày tạo', 'o_ngaytao'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Bộ phận', 'o_bophan')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 6: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('TẠO PHIẾU GIAO VIỆC')
    d.step('Bước 1: Truy cập vào màn hình Phiếu chờ giao việc, chọn thẻ chứa chứng từ cần giao việc (PHẦN 1).')
    d.step(['Bước 2: Ở cột Hành động, bấm ', '@btn_taopgv_row'])
    d.step('Bước 3: Hệ thống mở màn Tạo phiếu giao việc với chứng từ đã chọn sẵn.')
    d.img('40_create_pgv', 'Màn hình Tạo phiếu giao việc')
    d.step('Bước 4: Nhập thông tin phiếu giao việc và lưu (theo HDSD Phiếu giao việc).')
    d.sub(['Hoặc bấm ', '@btn_quaylai', ' để trở về đúng thẻ của Phiếu chờ giao việc.'])

    d.phan('TỪ CHỐI TIẾP NHẬN XỬ LÝ')
    d.step(['Bước 1: Ở thẻ ', '@tab_contract', ' hoặc ', '@tab_addition_annex', ', tại cột Hành động bấm ', '@btn_tuchoi_row'])
    d.step('Bước 2: Hệ thống hiện hộp “Từ chối tiếp nhận xử lý”.')
    d.img('30_reject', 'Hộp Từ chối tiếp nhận xử lý')
    d.step(['Bước 3: Nhập Lý do từ chối ', '@o_lydo', ' (bắt buộc)'])
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm.'])

    d.phan('ĐÓNG HỢP ĐỒNG')
    d.step(['Bước 1: Ở thẻ ', '@tab_contract', ', tại cột Hành động bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_dong'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Đóng hợp đồng”.')
    d.img('31_close', 'Hộp xác nhận Đóng hợp đồng')
    d.step(['Bước 3: Bấm ', '@btn_confirm_dong', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm.'])

    d.phan('HỦY DUYỆT HỢP ĐỒNG')
    d.step(['Bước 1: Ở thẻ ', '@tab_contract', ', tại cột Hành động bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_huyduyet'])
    d.step('Bước 2: Hệ thống hiện hộp “Hủy duyệt hợp đồng”.')
    d.img('32_unapprove', 'Hộp Hủy duyệt hợp đồng')
    d.step('Bước 3: Nhập Lý do hủy duyệt (bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_huyduyet', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm.'])

    d.phan('QUYẾT TOÁN HỢP ĐỒNG VÀ CÁC LIÊN KẾT SANG HỆ THỐNG ERP')
    d.step(['Bước 1: Ở thẻ ', '@tab_contract', ', tại cột Hành động bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_quyettoan'])
    d.img('01b_row_more', 'Menu Hành động khác của hợp đồng')
    d.step('Bước 2: Hệ thống mở màn quyết toán hợp đồng của hệ thống ERP ở thẻ trình duyệt mới.')
    d.sub(['Ở thẻ ', '@tab_assembly', ', bấm ', '@btn_xuat1_row', ' để xuất Excel 1 phiếu yêu cầu lắp đặt (hệ thống ERP)'])
    d.sub(['Hoặc bấm số phiếu ', '@link_sophieu_ld', ' / số hợp đồng ', '@link_sohd', ' để xem ở hệ thống ERP.'])

    d.phan('XEM CHI TIẾT')
    d.step(['Bước 1: Ở thẻ ', '@tab_warranty', ', bấm vào Mã phiếu ', '@link_mabh', '. Hệ thống mở màn Chi tiết phiếu bảo hành.'])
    d.sub(['Hoặc ở thẻ ', '@tab_other', ', bấm vào Số phiếu ', '@link_sophieu_gvk', ' để mở Chi tiết phiếu yêu cầu giao việc khác'])
    d.img('60_detail_bh', 'Màn hình Chi tiết phiếu bảo hành')
    d.step(['Bước 2: Bấm ', '@btn_quaylai', ' để về Phiếu chờ giao việc.'])

    d.phan('IN PHIẾU YÊU CẦU LẮP ĐẶT BÀN GIAO')
    d.step(['Bước 1: Ở thẻ ', '@tab_assembly', ', tại cột Hành động bấm ', '@btn_in_row'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('50_print', 'Cửa sổ Xem trước phiếu yêu cầu lắp đặt bàn giao')
    d.step(['Bước 3: Bấm ', '@btn_in_popup', ' để in'])
    d.sub(['Hoặc bấm ', '@btn_x_print', ' để đóng.'])

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
