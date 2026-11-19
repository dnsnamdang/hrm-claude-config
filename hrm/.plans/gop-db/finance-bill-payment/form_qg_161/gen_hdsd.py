# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu chi tiền (STT 161, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu chi tiền.docx (+ .pdf, render/ để soát)
Khuôn: ../../finance-product-import-direct-transfer/form_qg/gen_hdsd.py (màn 27 đã duyệt).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu chi tiền'
SHOTS = os.path.join(HERE, 'hdsd_shots')
ICON27 = os.path.join(HERE, '..', '..', 'finance-product-import-direct-transfer', 'form_qg', 'hdsd_shots', 'icons')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)

THUAT_NGU = [
    ['Phiếu chi tiền', 'Chứng từ ghi nhận khoản tiền doanh nghiệp chi ra. Mã phiếu do hệ thống tự sinh, ví dụ '
                       'TPE.PC0826.00025.'],
    ['Luồng lập từ Đề nghị thanh toán', 'Áp dụng với các loại chi: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi '
                                        'thưởng NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận '
                                        'chuyển NCC. Chọn phiếu đề nghị, chỉ Thủ quỹ duyệt.'],
    ['Luồng Chi thu nhập cho nhân viên', 'Lập trực tiếp theo phòng ban, không qua phiếu đề nghị. Duyệt 2 cấp: Kế toán '
                                         'trưởng rồi Thủ quỹ.'],
    ['Tài khoản có / Tài khoản nợ', 'Tài khoản ghi bên Có (cả phiếu) / bên Nợ (từng dòng chi tiết) của bút toán.'],
    ['Số tiền đề nghị chi', 'Số tiền lấy từ phiếu đề nghị thanh toán, chỉ đọc.'],
    ['Số tiền chi', 'Số tiền kế toán chốt sẽ chi, không được lớn hơn Số tiền đề nghị chi của dòng.'],
    ['Số tiền thực chi', 'Số tiền người duyệt xác nhận chi thật, nhập trong cửa sổ Duyệt.'],
    ['Số dư', 'Số tiền thu nhập còn lại của từng nhân viên, được phép âm (truy thu).'],
    ['Hình thức thanh toán', 'TM (tiền mặt) hoặc CK (chuyển khoản).'],
    ['Trạng thái Đang tạo', 'Phiếu nháp. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ KT trưởng duyệt', 'Chỉ loại Chi thu nhập cho nhân viên, chờ Kế toán trưởng duyệt.'],
    ['Trạng thái Chờ chi tiền', 'Chờ Thủ quỹ duyệt (cấp cuối).'],
    ['Trạng thái Đã duyệt', 'Thủ quỹ đã duyệt, đã ghi sổ kế toán. Chỉ xem, in, xuất Excel.'],
    ['Trạng thái Hủy', 'Người duyệt đã hủy phiếu kèm lý do.'],
]

PHIEN_BAN = [
    ['1.0', '03/09/2026', 'Ban hành lần đầu cho màn Phiếu chi tiền (phân hệ Tài chính, nhóm Quản lý tiền).'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Xem tất cả phiếu chi của tổng công ty / Xem tất cả phiếu chi của công ty. Phiếu do chính mình lập luôn xem được.'],
    ['Lập, sửa, xóa phiếu', 'Kế toán thanh toán. Sửa, xóa: chỉ người lập, phiếu đang ở trạng thái Đang tạo.'],
    ['Duyệt, hủy cấp 1', 'Kế toán trưởng duyệt phiếu chi, cùng công ty, phiếu Chờ KT trưởng duyệt.'],
    ['Duyệt, hủy cấp cuối', 'Thủ quỹ duyệt phiếu chi, cùng công ty, phiếu Chờ chi tiền.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=[os.path.join(SHOTS, 'icons'), ICON27])
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Quản lý tiền', 'menu_nhom'),
              ('Thanh toán tiền mặt', 'menu_thanhtoan'), ('Phiếu chi', 'menu_muc')],
        o_nhanh='mã phiếu chi',
        bo_loc=[('Mã phiếu đề nghị chi', 'o_madenghi'), ('Loại chi', 'o_loaichi'), ('Trạng thái', 'o_trangthai'),
                ('Người lập', 'o_nguoilap'), ('Người đề nghị', 'o_nguoidenghi'), ('Phòng ban', 'o_phongban'),
                ('Khách hàng / Nhà cung cấp', 'o_doitac'), ('Số tiền', 'o_sotien'), ('Ngày lập', 'o_ngaylap')])

    # PHẦN 2 — Tạo mới (2 nhánh)
    d.phan('TẠO MỚI PHIẾU CHI')
    d.h2('1. Lập từ Đề nghị thanh toán')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.sub('Hoặc tại màn Đề nghị thanh toán, bấm Tạo phiếu chi ở phiếu đề nghị: form nạp sẵn phiếu đề nghị đó, '
          'bỏ qua Bước 3–4.')
    d.step('Bước 3: Chọn Loại chi (bắt buộc): Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi '
           'thưởng thực hiện hợp đồng, Chi khác hoặc Thanh toán chi phí vận chuyển NCC.')
    d.step(['Bước 4: Bấm vào ô ', '@o_sophieudenghi', '. Hệ thống mở cửa sổ “Chọn phiếu đề nghị chi”, bấm vào dòng '
            'phiếu cần chọn.'])
    d.sub(['Hoặc bấm ', '@btn_dong', ' để không chọn.'])
    d.img('11_request', 'Cửa sổ Chọn phiếu đề nghị chi')
    d.step('Bước 5: Nhập thông tin chung:')
    d.sub('Tài khoản có (bắt buộc khi gửi duyệt): chọn trong danh sách.')
    d.sub('Người nhận (bắt buộc khi gửi duyệt): nhập chữ, tối đa 255 ký tự.')
    d.sub('Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi: tự điền theo phiếu đề nghị.')
    d.step('Bước 6: Ở bảng Chi tiết, nhập từng dòng:')
    d.sub('Tài khoản nợ (bắt buộc khi gửi duyệt): chọn trong danh sách.')
    d.sub('Số tiền chi (bắt buộc): chỉ nhập số, không lớn hơn Số tiền đề nghị chi của dòng; dấu phẩy ngăn hàng '
          'nghìn, dấu chấm ngăn phần thập phân (ví dụ 1,200.5).')
    d.sub('Ghi chú (tùy chọn).')
    d.step(['Bước 7: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để gửi Thủ quỹ duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần chọn Loại chi).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])
    d.h2('2. Chi thu nhập cho nhân viên')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Chọn Loại chi = Chi thu nhập cho nhân viên.')
    d.step(['Bước 4: Chọn ', '@o_phongbanchi', ' (bắt buộc). Hệ thống nạp bảng thu nhập của từng nhân viên.'])
    d.img('15_employee_table', 'Màn Tạo mới loại Chi thu nhập cho nhân viên sau khi chọn Phòng ban chi')
    d.step('Bước 5: Nhập thông tin chung (bắt buộc khi gửi duyệt): Người nhận, Hình thức thanh toán, Loại tiền, '
           'Tỷ giá, Lý do chi.')
    d.step('Bước 6: Ở tab Chi tiết, bỏ tích nhân viên không chi; kiểm tra Số tài khoản nợ và Số tiền chi của từng '
           'dòng.')
    d.sub('Hoặc mở tab Chi tiết vụ việc để nhập Số tiền chi theo 6 khoản thu nhập; tổng 6 khoản phải bằng Số tiền '
          'chi của dòng, mỗi khoản không vượt số dư.')
    d.step(['Bước 7: Bấm ', '@btn_luuguiduyet', ', chọn ', '@btn_confirm_xacnhan', ' để gửi Kế toán trưởng duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu chi tiền”.')
    d.img('16_edit', 'Màn hình Sửa phiếu chi tiền')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ' để lưu và gửi duyệt,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', img='20_delete', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Duyệt 2 cấp
    d.phan('DUYỆT PHIẾU CHI')
    d.h2('1. Kế toán trưởng duyệt (loại Chi thu nhập cho nhân viên)')
    d.step('Bước 1: Bấm vào Mã phiếu của phiếu Chờ KT trưởng duyệt để mở màn chi tiết.')
    d.step(['Bước 2: Bấm ', '@btn_duyetphieuchi', '. Hệ thống mở cửa sổ “Duyệt phiếu chi thu nhập nhân viên”.'])
    d.img('19_approve_employee', 'Cửa sổ Duyệt phiếu chi thu nhập nhân viên')
    d.step('Bước 3: Nhập Số tiền thực chi của từng khoản (bắt buộc) và Ghi chú (tùy chọn, tối đa 500 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_duyet', ', chọn ', '@btn_confirm_duyet', ' để chuyển phiếu sang Thủ quỹ'])
    d.sub(['Hoặc bấm ', '@btn_dong_approve', ' nếu chưa duyệt.'])
    d.h2('2. Thủ quỹ duyệt (cấp cuối)')
    d.step('Bước 1: Bấm vào Mã phiếu của phiếu Chờ chi tiền để mở màn chi tiết.')
    d.sub(['Hoặc ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_duyet'])
    d.step(['Bước 2: Bấm ', '@btn_duyetphieuchi', '. Hệ thống mở cửa sổ “Duyệt phiếu chi tiền”.'])
    d.img('18_approve', 'Cửa sổ Duyệt phiếu chi tiền')
    d.step('Bước 3: Nhập Số tiền thực chi của từng dòng (bắt buộc, không lớn hơn Số tiền đề nghị chi) và Ghi chú '
           '(tùy chọn).')
    d.step(['Bước 4: Bấm ', '@btn_duyet', ', chọn ', '@btn_confirm_duyet', ' để duyệt. Phiếu được ghi sổ kế toán, '
            'không hoàn tác được.'])
    d.sub(['Hoặc bấm ', '@btn_dong_approve', ' nếu chưa duyệt.'])

    # PHẦN 6 — Hủy
    d.phan('HỦY PHIẾU CHI')
    d.step('Bước 1: Mở màn chi tiết của phiếu đang chờ đúng cấp duyệt của mình (như PHẦN 5).')
    d.step(['Bước 2: Bấm ', '@btn_huyphieuchi', '. Hệ thống mở cửa sổ “Hủy phiếu chi tiền”.'])
    d.img('21_cancel', 'Cửa sổ Hủy phiếu chi tiền')
    d.step('Bước 3: Nhập Lý do hủy (bắt buộc, tối đa 500 ký tự) và Ghi chú (tùy chọn).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_huy', ' để hủy phiếu'])
    d.sub(['Hoặc bấm ', '@btn_dong_cancel', ' nếu muốn bỏ qua.'])

    # PHẦN 7 — Lịch sử
    d.lich_su('Mã phiếu', img='24_history', cap='Cửa sổ Lịch sử thay đổi của phiếu chi')

    # PHẦN 8 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu chi”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu chi')
    d.step('Bước 3: Phiếu đã hủy hiện dải vàng đầu màn với Lý do hủy và Ghi chú.')
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 9 — In
    d.phan('IN PHIẾU')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in (2 liên).')
    d.img('23_print', 'Cửa sổ Xem trước phiếu chi')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    # PHẦN 10 — Xuất Excel một phiếu
    d.phan('XUẤT EXCEL PHIẾU CHI')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_xuatexcel_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xuatexcel'])
    d.img('01b_list_actions', 'Các nút thao tác trên dòng phiếu chi')
    d.step('Bước 2: Mở tệp phieu_chi_tien_<mã phiếu>.xlsx vừa tải về.')

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
