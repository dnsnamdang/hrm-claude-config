# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu yêu cầu vận chuyển, bốc xếp (form chuẩn Danh mục quốc gia, 30/10/2026).

Chạy: python gen_hdsd.py  → HDSD_Phieu yeu cau van chuyen boc xep.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu yêu cầu vận chuyển, bốc xếp'
SHOTS = os.path.join(HERE, 'ycvc_shots')
OUT = os.path.join(HERE, 'HDSD_Phieu yeu cau van chuyen boc xep.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_ycvc')   # PDF + ảnh soát, không để trong repo

THUAT_NGU = [
    ['Phiếu yêu cầu vận chuyển', 'Phiếu đề nghị thủ kho bố trí vận chuyển, bốc xếp, mã dạng TPE.YCVC1026.00004.'],
    ['Phiếu YCXH', 'Phiếu yêu cầu xuất hàng — nguồn lấy khách hàng, địa điểm giao và danh sách hàng.'],
    ['Thủ kho', 'Người duyệt / từ chối phiếu, là thủ kho của kho xuất hàng trên phiếu YCXH.'],
    ['Đang tạo', 'Phiếu lưu nháp, người lập còn sửa / xóa được.'],
    ['Chờ duyệt', 'Phiếu đã gửi, chờ thủ kho xử lý.'],
    ['Đã duyệt', 'Thủ kho đã đồng ý.'],
    ['Từ chối', 'Thủ kho không đồng ý, kèm lý do; người lập sửa và gửi lại được.'],
]
PHIEN_BAN = [['1.0', '30/10/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, xuất Excel, xem lịch sử',
     'Phiếu do mình lập hoặc mình là thủ kho luôn xem được. Xem rộng hơn cần một trong các quyền: Xem tất cả phiếu yêu cầu '
     'vận chuyển của tổng công ty / của công ty / của phòng ban / của bộ phận.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu; phiếu Đang tạo hoặc Từ chối.'],
    ['Duyệt, từ chối', 'Thủ kho của kho xuất hàng; phiếu Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.truy_cap(
        menu=[('Bán hàng', 'menu_phanhe'), ('Yêu cầu', 'menu_yeucau'), ('Hàng hóa', 'menu_hanghoa'),
              ('YC vận chuyển, bốc xếp', 'menu_muc')],
        o_nhanh='mã phiếu, số hợp đồng hoặc mã phiếu YCXH',
        bo_loc=[('Trạng thái', 'o_trangthai'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Bộ phận', 'o_bophan'),
                ('Khách hàng', 'o_khachhang'), ('Hợp đồng', 'o_hopdong'), ('Người tạo', 'o_nguoitao'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Thêm mới
    d.phan('LẬP PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC XẾP')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10c_filled', 'Màn hình Tạo phiếu yêu cầu vận chuyển, bốc xếp')
    d.step(['Bước 3: Bấm vào ô ', '@o_hopdong_form', ', tìm theo số hoặc Loại hợp đồng, bấm vào dòng cần chọn (bắt buộc).'])
    d.sub(['Hoặc bấm ', '@btn_dong_popup', ' để không chọn.'])
    d.step(['Bước 4: Bấm vào ô ', '@o_ycxh_form', ', bấm vào phiếu yêu cầu xuất hàng cần vận chuyển (bắt buộc). Khách hàng, '
            'người liên hệ, địa điểm giao và bảng hàng tự điền.'])
    d.step('Bước 5: Nhập Thời gian vận chuyển, Ghi chú (tùy chọn).')
    d.step('Bước 6: Nhập khối Bốc xếp: Tổng số kiện (số nguyên), Phương thức, Địa điểm, Thời gian bốc xếp (tùy chọn).')
    d.step(['Bước 7: Bấm ', '@btn_themtailieu', ' để đính kèm file (tùy chọn; pdf, xlsx, xls, jpeg, jpg, png, tối đa 20 MB).'])
    d.step('Bước 8: Ở bảng Chi tiết, nhập Số kiện từng dòng hàng (tùy chọn, số nguyên).')
    d.step(['Bước 9: Bấm ', '@btn_guiduyet', ' để gửi thủ kho duyệt'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo hoặc Từ chối do mình lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu yêu cầu vận chuyển, bốc xếp”.')
    d.img('19_edit', 'Màn hình Sửa phiếu yêu cầu vận chuyển, bốc xếp')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2). Phiếu Từ chối: đọc Lý do từ chối rồi sửa lại.')
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

    # PHẦN 5 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu yêu cầu vận chuyển, bốc xếp”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu yêu cầu vận chuyển, bốc xếp')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 6 — Duyệt
    d.phan('DUYỆT PHIẾU')
    d.step('Bước 1: Truy cập vào màn hình, lọc Trạng thái Chờ duyệt.')
    d.step(['Bước 2: Bấm ', '@btn_duyet_row', ' ở cột Hành động (hoặc bấm Mã phiếu) để mở màn chi tiết.'])
    d.step(['Bước 3: Bấm ', '@btn_duyet', '. Hệ thống hiện hộp “Xác nhận duyệt”.'])
    d.img('14_approve', 'Hộp xác nhận duyệt phiếu')
    d.step(['Bước 4: Bấm ', '@btn_confirm_duyet', ' để duyệt'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 7 — Từ chối
    d.phan('TỪ CHỐI PHIẾU')
    d.step('Bước 1: Mở màn chi tiết của phiếu Chờ duyệt (Bước 1, 2 PHẦN 6).')
    d.step(['Bước 2: Bấm ', '@btn_tuchoi', '. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu vận chuyển”.'])
    d.img('15_reject', 'Cửa sổ Từ chối phiếu yêu cầu vận chuyển')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_huy_reject', ' nếu muốn hủy.'])

    # PHẦN 8 — Lịch sử
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.xuat_excel()
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
