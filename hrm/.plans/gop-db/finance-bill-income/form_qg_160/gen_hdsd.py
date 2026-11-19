# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu thu tiền (form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu thu tiền.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py — khuôn chép từ màn 27.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu thu tiền'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Phiếu thu tiền', 'Chứng từ kế toán lập từ một phiếu đề nghị thu tiền đang chờ duyệt, ghi nhận khoản tiền thực tế '
                       'thu về. Mã phiếu do hệ thống sinh tự động, ví dụ TPE.PT1026.00067.'],
    ['Phiếu đề nghị thu tiền', 'Chứng từ do người kinh doanh lập để đề nghị kế toán thu tiền. Một phiếu đề nghị chỉ '
                               'lập được đúng một phiếu thu.'],
    ['Dòng chi tiết', 'Một dòng trong bảng Chi tiết, lấy nguyên từ phiếu đề nghị. Không thêm, không xóa dòng được.'],
    ['Tài khoản nợ', 'Tài khoản ghi bên Nợ của bút toán (thường là tài khoản tiền), chọn một lần cho cả phiếu.'],
    ['Số tài khoản có', 'Tài khoản ghi bên Có của bút toán, chọn riêng cho từng dòng chi tiết.'],
    ['Số tiền duyệt thu', 'Số tiền kế toán chốt sẽ thu cho từng dòng. Tổng cột này là cột Số tiền ở màn danh sách.'],
    ['Số tiền thực thu', 'Số tiền thủ quỹ thực nhận, nhập ở màn chi tiết trước khi duyệt; không lớn hơn số tiền '
                         'duyệt thu của dòng đó.'],
    ['Phân bổ', 'Thủ quỹ nhập tổng tiền thực nhận, hệ thống tự rải xuống cột Số tiền thực thu từ trên xuống.'],
    ['Trạng thái Đang tạo', 'Phiếu lưu nháp. Chỉ người lập nhìn thấy, sửa và xóa được.'],
    ['Trạng thái Chờ duyệt', 'Phiếu đã gửi, chờ thủ quỹ duyệt hoặc hủy. Không sửa, không xóa được.'],
    ['Trạng thái Đã duyệt', 'Thủ quỹ đã duyệt, hệ thống đã ghi bút toán vào sổ kế toán. Chỉ xem, in, xuất Excel.'],
    ['Trạng thái Hủy', 'Thủ quỹ đã hủy phiếu kèm lý do; phiếu đề nghị tương ứng cũng chuyển sang Hủy.'],
]

PHIEN_BAN = [
    ['1.0', '03/09/2026', 'Ban hành lần đầu cho màn Phiếu thu tiền (phân hệ Tài chính, nhóm Quản lý tiền).'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Xem tất cả phiếu thu của tổng công ty / Xem tất cả phiếu thu của công ty. Không có quyền nào thì chỉ thấy phiếu '
     'do chính mình lập.'],
    ['Tạo mới, sửa phiếu', 'Kế toán thanh toán. Sửa chỉ với phiếu Đang tạo.'],
    ['Xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Duyệt, hủy phiếu', 'Thủ quỹ duyệt phiếu thu, phiếu đang ở trạng thái Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Quản lý tiền', 'menu_nhom'),
              ('Thanh toán tiền mặt', 'menu_thanhtoan'), ('Phiếu thu', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Công ty, Phòng ban, Bộ phận', 'o_congty'), ('Mã phiếu đề nghị thu', 'o_madenghi'),
                ('Loại thu', 'o_loaithu'), ('Trạng thái', 'o_trangthai'), ('Người tạo', 'o_nguoitao'),
                ('Người đề nghị', 'o_nguoidenghi'), ('Khách hàng (gõ tối thiểu 2 ký tự)', 'o_khachhang'),
                ('Số hợp đồng/đơn hàng', 'o_hopdong'), ('Số tiền từ – đến', 'o_sotien'),
                ('Ngày lập từ – đến', 'o_ngaylap')])

    # PHẦN 2 — Tạo mới
    d.phan('TẠO MỚI PHIẾU THU')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Thêm phiếu thu tiền')
    d.step(['Bước 3: Bấm vào ô Số phiếu đề nghị ', '@o_sophieudenghi',
            ' (bắt buộc). Hệ thống mở cửa sổ “Chọn phiếu đề nghị thu”.'])
    d.img('11_request', 'Cửa sổ Chọn phiếu đề nghị thu')
    d.step('Bước 4: Bấm vào dòng phiếu đề nghị cần lập phiếu thu. Hệ thống tự điền Loại thu, Loại tiền, Người đề nghị, '
           'Phòng ban, Lý do thu và bảng Chi tiết.')
    d.sub(['Hoặc bấm ', '@btn_dong_req', ' để không chọn phiếu.'])
    d.step('Bước 5: Nhập thông tin chung:')
    d.sub('Tài khoản nợ (bắt buộc): chọn trong danh sách, hệ thống chọn sẵn tài khoản tiền mặt.')
    d.sub('Người nộp (bắt buộc): nhập chữ, tối đa 255 ký tự.')
    d.sub('Tỷ giá (VND) (bắt buộc): chỉ nhập số; phiếu tiền VNĐ cố định bằng 1.')
    d.sub('Ghi chú (tùy chọn): nhập chữ, tối đa 1000 ký tự.')
    d.step('Bước 6: Nhập thông tin từng dòng ở bảng Chi tiết:')
    d.sub('Số tài khoản có (bắt buộc): chọn trong danh sách.')
    d.sub('Số tiền duyệt thu (bắt buộc): chỉ nhập số, không âm; dấu phẩy ngăn hàng nghìn (ví dụ 2,556,360).')
    d.sub('Ghi chú của dòng (tùy chọn).')
    d.step(['Bước 7: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để gửi thủ quỹ duyệt,'])
    d.sub(['Hoặc ', '@btn_luu_form', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu thu tiền”.')
    d.img('12_edit', 'Màn hình Sửa phiếu thu tiền')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Tạo mới ở PHẦN 2). Bấm ô Số phiếu đề nghị nếu cần đổi '
           'sang phiếu đề nghị khác.')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để lưu và gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luu_form', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt
    d.phan('DUYỆT PHIẾU THU')
    d.step(['Bước 1: Bấm ', '@btn_duyet_row', ' ở cột Hành động của phiếu Chờ duyệt để mở màn chi tiết.'])
    d.sub('Hoặc bấm vào Mã phiếu của phiếu Chờ duyệt.')
    d.img('15_approve', 'Màn hình chi tiết phiếu Chờ duyệt')
    d.step('Bước 2: Nhập Số tiền thực thu của từng dòng (bắt buộc): chỉ nhập số, không âm, không lớn hơn Số tiền duyệt '
           'thu của dòng đó.')
    d.sub(['Hoặc nhập tổng tiền thực nhận vào ô ', '@o_phanbo', ', bấm ', '@btn_phanbo',
           ' để hệ thống tự rải xuống từng dòng.'])
    d.step(['Bước 3: Bấm ', '@btn_duyet', '. Hệ thống hiện hộp xác nhận “Xác nhận duyệt”.'])
    d.img('15b_confirm', 'Hộp xác nhận duyệt phiếu thu')
    d.step(['Bước 4: Bấm ', '@btn_confirm_duyet', ' để duyệt. Hệ thống ghi bút toán vào sổ kế toán, không hoàn tác '
            'được.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    # PHẦN 6 — Hủy
    d.phan('HỦY PHIẾU THU')
    d.step('Bước 1: Mở màn chi tiết của phiếu Chờ duyệt (như Bước 1 PHẦN 5).')
    d.step(['Bước 2: Bấm ', '@btn_huyphieu', '. Hệ thống mở cửa sổ “Hủy phiếu thu tiền”.'])
    d.img('16_cancel', 'Cửa sổ Hủy phiếu thu tiền')
    d.step('Bước 3: Nhập Lý do hủy (bắt buộc, tối đa 1000 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_huy', ' để hủy. Phiếu đề nghị tương ứng cũng chuyển sang Hủy và không lập '
            'lại được phiếu thu khác.'])
    d.sub(['Hoặc bấm ', '@btn_dong_cancel', ' nếu muốn bỏ qua.'])

    # PHẦN 7 — Lịch sử
    d.lich_su('Mã phiếu', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu thu')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU THU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu thu tiền”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu thu tiền')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU THU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Xem trước phiếu thu” gồm đủ 2 liên.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu thu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 10 — Xuất Excel 1 phiếu
    d.phan('XUẤT EXCEL PHIẾU THU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_excel_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_excel'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuatexcel'])
    d.img('20_export', 'Nút Xuất Excel trên màn chi tiết phiếu thu')
    d.step('Bước 2: Hệ thống tải về tệp Phieu-thu-tien-<mã phiếu>.xlsx.')
    d.step('Bước 3: Mở file Excel đã tải về.')

    # PHẦN 11..12
    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    pdf = os.path.splitext(out)[0] + '.pdf'
    size = finalize_word(out, pdf)
    print('docx', out, size)
    print('TOC:')
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(HERE, 'out', 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
