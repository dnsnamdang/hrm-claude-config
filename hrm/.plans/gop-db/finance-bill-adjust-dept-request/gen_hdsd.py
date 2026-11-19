# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu yêu cầu điều chỉnh công nợ (form chuẩn Danh mục quốc gia, 30/10/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu yeu cau dieu chinh cong no.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu yêu cầu điều chỉnh công nợ'
SHOTS = os.path.join(HERE, 'dcbn_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu yeu cau dieu chinh cong no.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_dcbn')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu yêu cầu điều chỉnh công nợ', 'Phiếu đề nghị chuyển công nợ sang khách hàng / nhà cung cấp, hợp đồng khác; '
                                          'mã dạng TPE.DNDCCN1026.00401.'],
    ['Điều chỉnh từ', 'Khách hàng / nhà cung cấp, hợp đồng và số tiền công nợ bị chuyển đi.'],
    ['Điều chỉnh đến', 'Nơi nhận công nợ; một dòng “từ” có thể chia cho nhiều dòng “đến”.'],
    ['Đang tạo', 'Phiếu lưu nháp, người lập còn sửa / xóa / gửi duyệt được.'],
    ['Chờ tạo phiếu kế toán', 'Phiếu đã gửi, chờ Kế toán thanh toán xử lý.'],
    ['Đã tạo / Đã duyệt phiếu kế toán', 'Kế toán đã lập / đã duyệt phiếu kế toán từ phiếu này.'],
    ['Từ chối', 'Kế toán không duyệt, kèm lý do; người lập sửa và gửi lại được.'],
]
PHIEN_BAN = [['1.0', '30/10/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do mình lập luôn xem được. Xem rộng hơn cần một trong các quyền: Xem tất cả phiếu yêu cầu điều chỉnh của tổng '
     'công ty / của công ty / của phòng ban / của bộ phận.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa, gửi duyệt', 'Người lập phiếu; phiếu Đang tạo hoặc Từ chối.'],
    ['Màn chờ duyệt, Từ chối, Tạo phiếu kế toán', 'Quyền Kế toán thanh toán, cùng công ty với người lập; phiếu Chờ tạo phiếu kế toán.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    # PHẦN 1 — 2 lối vào
    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.p('Cách 1: Từ phân hệ Tài chính:')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Khởi tạo ', '@menu_khoitao', ', nhóm Khởi tạo phiếu yêu cầu - '
            'Công nợ - Thu - Chi ', '@menu_nhom_khoitao', ', chọn Phiếu yêu cầu điều chỉnh công nợ ', '@menu_muc'])
    d.p('Cách 2: Từ phân hệ Bán hàng:')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe_banhang', ', tại menu Yêu cầu ', '@menu_yeucau', ', nhóm Công nợ - Thu - Chi ',
            '@menu_congno', ', chọn YC điều chỉnh công nợ ', '@menu_muc_sale'])
    d.img('01_list', 'Màn hình Phiếu yêu cầu điều chỉnh công nợ')
    d.step(['Bước 2: Nhập mã phiếu vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Loại phiếu', 'o_loaiphieu'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Bộ phận', 'o_bophan'),
                   ('Số phiếu báo có', 'o_phieubaoco'), ('Khách hàng / Nhà cung cấp', 'o_khncc'),
                   ('Hợp đồng điều chỉnh từ', 'o_hdtu'), ('Hợp đồng điều chỉnh đến', 'o_hdden'), ('Người tạo', 'o_nguoitao'),
                   ('Người duyệt', 'o_nguoiduyet'), ('Số tiền', 'o_sotien'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu điều chỉnh công nợ (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10c_filled', 'Màn hình Tạo phiếu yêu cầu điều chỉnh công nợ')
    d.step('Bước 3: Chọn Loại phiếu (bắt buộc; mặc định Điều chỉnh công nợ khách hàng). Loại nhà cung cấp: chọn Tiền tệ, '
           'nhập Tỷ giá nếu khác VNĐ.')
    d.step('Bước 4: Nhập Diễn giải (bắt buộc khi gửi duyệt).')
    d.step(['Bước 5: Ở bảng Chi tiết, bấm ', '@btn_themdong', ' để thêm một nhóm điều chỉnh.'])
    d.step(['Bước 6: Bên Điều chỉnh từ: bấm ô ', '@o_khachhang_form', ' chọn khách hàng (bắt buộc), bấm ô ', '@o_hopdong_form',
            ' chọn hợp đồng, nhập Số tiền (bắt buộc, lớn hơn 0).'])
    d.step('Bước 7: Bên Điều chỉnh đến: chọn khách hàng, hợp đồng (bắt buộc khi gửi duyệt), nhập Số tiền. Tổng “đến” phải '
           'bằng số tiền “từ” (dòng Số tiền còn lại về 0).')
    d.sub('Hoặc bấm Thêm dòng điều chỉnh để chia công nợ cho nhiều nơi nhận.')
    d.sub(['Hoặc bấm ', '@btn_xoanhom', ' để bỏ cả nhóm điều chỉnh.'])
    d.step(['Bước 8: Bấm ', '@btn_guiduyet', ' để gửi Kế toán thanh toán'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu điều chỉnh công nợ.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo hoặc Từ chối do mình lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu yêu cầu điều chỉnh công nợ”.')
    d.img('19_edit', 'Màn hình Sửa phiếu yêu cầu điều chỉnh công nợ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc như PHẦN 2). Phiếu Từ chối: đọc Ghi chú không duyệt rồi sửa lại.')
    d.step(['Bước 5: Bấm ', '@btn_guiduyet', ' để gửi duyệt'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.phan('XÓA')
    d.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đang tạo hoặc Từ chối do mình lập'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 5 — Xem chi tiết + Gửi duyệt từ chi tiết
    d.phan('XEM CHI TIẾT VÀ GỬI DUYỆT')
    d.step('Bước 1: Truy cập vào màn hình Phiếu yêu cầu điều chỉnh công nợ.')
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu yêu cầu điều chỉnh công nợ”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu yêu cầu điều chỉnh công nợ')
    d.step(['Bước 3: Phiếu Đang tạo / Từ chối do mình lập: bấm ', '@btn_guiduyet_detail', ' để gửi Kế toán thanh toán.'])
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 6 — Tạo phiếu kế toán
    d.phan('TẠO PHIẾU KẾ TOÁN (KẾ TOÁN THANH TOÁN)')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe', ', tại menu Chờ duyệt ', '@menu_choduyet', ', nhóm Phê duyệt - Công nợ - '
            'Thu - Chi ', '@menu_nhom_pheduyet', ', chọn Phiếu yêu cầu điều chỉnh công nợ chờ duyệt ', '@menu_muc_choduyet'])
    d.step(['Bước 2: Bấm ', '@btn_taopktoan_row', ' ở cột Hành động'])
    d.sub(['Hoặc bấm Mã phiếu để mở màn chi tiết, chọn ', '@btn_taopktoan'])
    d.step('Bước 3: Hệ thống mở màn “Tạo phiếu kế toán” với phiếu yêu cầu điền sẵn.')
    d.img('21_accounting_create', 'Màn hình Tạo phiếu kế toán')
    d.step('Bước 4: Kiểm tra Thông tin chung, nhập đầy đủ trường bắt buộc: Ngày hạch toán (dd/mm/yyyy), Loại tiền, Tỷ giá (VND), Diễn giải.')
    d.step('Bước 5: Ở bảng Chi tiết, mỗi dòng chọn Số tài khoản, nhập Diễn giải (bắt buộc) và số Phát sinh nợ hoặc Phát sinh có; tổng nợ phải bằng tổng có.')
    d.step(['Bước 6: Bấm ', '@btn_pkt_luuduyet', ' để lưu và duyệt phiếu kế toán'])
    d.sub(['Hoặc ', '@btn_pkt_luunhap', ' để lưu nháp (chỉ cần Ngày hạch toán).'])
    d.sub(['Hoặc ', '@btn_pkt_luutieptuc', ' để lưu rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_pkt_quaylai', ' để không lưu thông tin.'])

    # PHẦN 7 — Từ chối
    d.phan('TỪ CHỐI PHIẾU (KẾ TOÁN THANH TOÁN)')
    d.step('Bước 1: Mở màn hình chờ duyệt như Bước 1 PHẦN 6.')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi_row', ' ở cột Hành động (mở màn chi tiết), rồi bấm ', '@btn_tuchoi'])
    d.step('Bước 3: Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu điều chỉnh công nợ”.')
    d.img('15_reject', 'Cửa sổ Từ chối phiếu yêu cầu điều chỉnh công nợ')
    d.step('Bước 4: Nhập Lý do từ chối (bắt buộc).')
    d.step(['Bước 5: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_huy_reject', ' nếu muốn hủy.'])

    # PHẦN 8 — In
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu điều chỉnh công nợ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 9 — Xuất Excel
    d.phan('XUẤT EXCEL')
    d.p('Cách 1: Xuất danh sách:')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống tải file Excel danh sách.'])
    d.img('20_export_toolbar', 'Nút Xuất Excel trên thanh công cụ')
    d.p('Cách 2: Xuất một phiếu:')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_xuat'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuat'])
    d.step('Bước 2: Mở file Excel đã tải.')

    # PHẦN 10 — Lịch sử
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

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
