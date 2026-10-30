# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu yêu cầu hạch toán bổ sung (form chuẩn Danh mục quốc gia, 30/10/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu yeu cau hach toan bo sung.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu yêu cầu hạch toán bổ sung'
SHOTS = os.path.join(HERE, 'htbs_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu yeu cau hach toan bo sung.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_htbs')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu yêu cầu hạch toán bổ sung', 'Phiếu đề nghị kế toán hạch toán bổ sung một khoản công nợ, mã PYCHTBS-002289.'],
    ['Loại yêu cầu', 'Điều chỉnh công nợ khách hàng, Điều chỉnh công nợ nhà cung cấp, Hạch toán công nợ NCC bảo hành, Hạch toán '
                     'công nợ NCC thiếu hàng, NCC hỗ trợ phát triển thị trường, Khác, Phối hợp kinh doanh.'],
    ['Chi tiết hạch toán', 'Bảng dòng của 2 loại Điều chỉnh công nợ: đối tượng, hợp đồng, số tiền, ghi chú.'],
    ['Đang tạo', 'Phiếu nháp hoặc bị từ chối trả về; người lập sửa / xóa / gửi duyệt được.'],
    ['Chờ duyệt', 'Phiếu đã gửi, chờ kế toán xử lý.'],
    ['Đang duyệt / Đã duyệt', 'Kế toán đã lập / đã duyệt phiếu kế toán.'],
]
PHIEN_BAN = [['1.0', '30/10/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do mình lập luôn xem được. Xem rộng hơn cần một trong các quyền: Xem phiếu yêu cầu hạch toán bổ sung - tổng công ty '
     '/ - công ty / - phòng ban / - bộ phận.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa, gửi duyệt', 'Người lập phiếu; phiếu Đang tạo.'],
    ['Từ chối', 'Kế toán thanh toán; phiếu Chờ duyệt.'],
    ['Lập phiếu kế toán', 'Kế toán thanh toán (loại 1–6) hoặc Kế toán của công ty phòng hỗ trợ (loại Phối hợp kinh doanh).'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.p('Cách 1: Từ phân hệ Tài chính:')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Khởi tạo ', '@menu_khoitao', ', nhóm Khởi tạo phiếu yêu cầu - '
            'Công nợ - Thu - Chi ', '@menu_nhom_khoitao', ', chọn Phiếu yêu cầu hạch toán bổ sung ', '@menu_muc'])
    d.p('Cách 2: Từ phân hệ Bán hàng:')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe_banhang', ', tại menu Yêu cầu ', '@menu_yeucau', ', nhóm Công nợ - Thu - Chi ',
            '@menu_congno', ', chọn YC hạch toán bổ sung ', '@menu_muc_sale'])
    d.img('01_list', 'Màn hình Phiếu yêu cầu hạch toán bổ sung')
    d.step(['Bước 2: Nhập số phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Loại yêu cầu', 'o_loai'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'),
                   ('Khách hàng / Nhà cung cấp', 'o_khncc'), ('Diễn giải', 'o_diengiai'), ('Phiếu xác nhận bảo hành', 'o_xnbh'),
                   ('Người tạo', 'o_nguoitao'), ('Người duyệt', 'o_nguoiduyet'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('LẬP PHIẾU YÊU CẦU HẠCH TOÁN BỔ SUNG')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu hạch toán bổ sung (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10e_filled', 'Màn hình Tạo phiếu yêu cầu hạch toán bổ sung')
    d.step('Bước 3: Chọn Loại yêu cầu (bắt buộc). Màn tự hiện các ô của loại đó.')
    d.step(['Bước 4: Loại Điều chỉnh công nợ khách hàng / nhà cung cấp: bấm ', '@btn_themdong', ', bấm ô ', '@o_khachhang_form',
            ' chọn đối tượng, bấm ô ', '@o_hopdong_form', ' chọn hợp đồng, nhập Số tiền và Ghi chú (đều bắt buộc).'])
    d.sub(['Hoặc bấm ', '@btn_xoadong', ' để bỏ dòng.'])
    d.sub('Loại khác: chọn Phiếu xác nhận bảo hành / Phiếu xử lý hàng thiếu / Nhà cung cấp / Đối tượng theo loại, nhập Số tiền '
          'và Diễn giải (bắt buộc).')
    d.step('Bước 5: Chọn Loại tiền, nhập Tỷ giá (bắt buộc, lớn hơn 0).')
    d.step(['Bước 6: Bấm ', '@btn_themtailieu', ' để đính kèm file (bắt buộc ít nhất 1 file khi gửi duyệt).'])
    d.step(['Bước 7: Bấm ', '@btn_guiduyet', ' để gửi kế toán'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần Loại yêu cầu).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu thông tin.'])

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu hạch toán bổ sung.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu yêu cầu hạch toán bổ sung”.')
    d.img('19_edit', 'Màn hình Sửa phiếu yêu cầu hạch toán bổ sung')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc như PHẦN 2). Phiếu bị từ chối: đọc Ghi chú duyệt rồi sửa lại.')
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', ' để gửi duyệt'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' nếu muốn hủy.'])

    d.phan('XÓA')
    d.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đang tạo do mình lập'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    d.phan('XEM CHI TIẾT VÀ GỬI DUYỆT')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu hạch toán bổ sung.')
    d.step('Bước 2: Bấm vào Số phiếu. Hệ thống mở màn “Chi tiết phiếu yêu cầu hạch toán bổ sung”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu yêu cầu hạch toán bổ sung')
    d.step(['Bước 3: Phiếu Đang tạo do mình lập: bấm ', '@btn_guiduyet_detail', ' để gửi kế toán.'])
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('LẬP PHIẾU KẾ TOÁN (KẾ TOÁN)')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Chờ duyệt ', '@menu_choduyet', ', nhóm Phê duyệt - Công nợ - '
            'Thu - Chi ', '@menu_nhom_pheduyet', ', chọn Phiếu yêu cầu hạch toán bổ sung chờ duyệt ', '@menu_muc_choduyet'])
    d.step(['Bước 2: Bấm ', '@btn_lappktoan_row', ' ở cột Hành động'])
    d.sub(['Hoặc bấm Số phiếu để mở màn chi tiết, chọn ', '@btn_lappktoan'])
    d.step('Bước 3: Hệ thống mở màn “Tạo phiếu kế toán” với phiếu yêu cầu điền sẵn.')
    d.img('21_accounting_create', 'Màn hình Tạo phiếu kế toán')
    d.step('Bước 4: Kiểm tra, lưu phiếu kế toán.')

    d.phan('TỪ CHỐI PHIẾU (KẾ TOÁN THANH TOÁN)')
    d.step('Bước 1: Mở màn chờ duyệt như Bước 1 PHẦN 6, bấm Số phiếu để mở màn chi tiết.')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu hạch toán bổ sung”.'])
    d.img('15_reject', 'Cửa sổ Từ chối phiếu yêu cầu hạch toán bổ sung')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận. Phiếu trở về Đang tạo.'])
    d.sub(['Hoặc bấm ', '@btn_huy_reject', ' nếu muốn hủy.'])

    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu hạch toán bổ sung')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.phan('XUẤT EXCEL')
    d.p('Cách 1: Xuất danh sách:')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca', ' / ', '@btn_bochonhet'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.p('Cách 2: Xuất một phiếu:')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuat'])
    d.step('Bước 2: Mở file Excel đã tải.')

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Số phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

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
