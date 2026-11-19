# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu ủy nhiệm chi (form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phiếu ủy nhiệm chi.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py
Ảnh + icon: hdsd_shots/ (capture.js, chụp DEV).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu ủy nhiệm chi'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_%s.docx' % TEN)
ICON27 = os.path.join(HERE, '..', '..', 'finance-product-import-direct-transfer', 'form_qg', 'hdsd_shots', 'icons')

THUAT_NGU = [
    ['Phiếu ủy nhiệm chi', 'Chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra bằng hình thức CHUYỂN KHOẢN. '
                           'Tài liệu này viết tắt là “phiếu”.'],
    ['Phiếu đề nghị thanh toán', 'Chứng từ do bộ phận nghiệp vụ lập để đề nghị chi tiền. Phiếu ủy nhiệm chi được lập '
                                 'từ phiếu này. Trong tài liệu gọi tắt là “phiếu đề nghị”.'],
    ['Phiếu chi tiền', 'Màn hình song sinh của Phiếu ủy nhiệm chi, dành cho các phiếu đề nghị thanh toán bằng TIỀN '
                       'MẶT. Hai màn không bao giờ nhận cùng một phiếu đề nghị.'],
    ['Đang tạo', 'Trạng thái phiếu nháp. Chỉ người lập nhìn thấy. Sửa và xóa được. Chưa ghi gì vào sổ kế toán.'],
    ['Đã hạch toán', 'Trạng thái phiếu đã ghi bút toán vào sổ kế toán. Không sửa, không xóa được nữa.'],
    ['Lưu nháp', 'Lưu phiếu tạm để làm tiếp sau. Chỉ bắt buộc chọn Loại chi.'],
    ['Lưu và duyệt', 'Chốt phiếu: ghi bút toán vào sổ kế toán ngay và khoá phiếu vĩnh viễn.'],
    ['Tài khoản có / Tài khoản nợ', 'Cặp tài khoản kế toán để ghi bút toán. Tài khoản có là tài khoản tiền bị trừ; '
                                    'tài khoản nợ là tài khoản công nợ được tất toán.'],
    ['Số tiền đề nghị chi / Số tiền duyệt chi', 'Số tiền bộ phận nghiệp vụ đề nghị và số tiền kế toán chốt chi. Số '
                                                'duyệt chi không được lớn hơn số đề nghị chi.'],
]

PHIEN_BAN = [
    ['1.0', '04/09/2026', 'Ban hành lần đầu cho màn Phiếu ủy nhiệm chi (phân hệ Tài chính).'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, xem lịch sử',
     'Một trong các quyền: Xem tất cả phiếu ủy nhiệm chi của tổng công ty / của công ty. Không có quyền nào vẫn xem '
     'được phiếu do chính mình lập hoặc duyệt. Phiếu Đang tạo chỉ người lập nhìn thấy.'],
    ['Lập phiếu, Lưu và duyệt', 'Quyền Kế toán thanh toán.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu có quyền Kế toán thanh toán, phiếu đang ở trạng thái Đang tạo.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS, icon_dirs=[os.path.join(SHOTS, 'icons'), ICON27])
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('Tài chính', 'menu_phanhe'), ('Quản lý tiền', 'menu_nhom'),
              ('Thanh toán tiền mặt', 'menu_thanhtoan'), ('Phiếu ủy nhiệm chi', 'menu_muc')],
        o_nhanh='mã phiếu',
        bo_loc=[('Mã phiếu', 'o_maphieu'), ('Mã phiếu đề nghị chi', 'o_madenghi'), ('Loại chi', 'o_loaichi'),
                ('Trạng thái', 'o_trangthai'), ('Người lập', 'o_nguoilap'), ('Người đề nghị', 'o_nguoidenghi'),
                ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Bộ phận', 'o_bophan'),
                ('Ngày lập', 'o_ngaylap')])

    # PHẦN 2 — Lập từ phiếu đề nghị
    d.phan('LẬP PHIẾU TỪ PHIẾU ĐỀ NGHỊ THANH TOÁN')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Thêm phiếu ủy nhiệm chi')
    d.step('Bước 3: Loại chi (bắt buộc): giữ “Chi trả nhà cung cấp” hoặc chọn loại chi khác.')
    d.step(['Bước 4: Bấm vào ô ', '@o_sophieudenghi', '. Hệ thống mở cửa sổ “Chọn phiếu đề nghị chi”.'])
    d.img('11_request', 'Cửa sổ Chọn phiếu đề nghị chi')
    d.step('Bước 5: Lọc theo Mã phiếu đề nghị, Loại chi, Người lập (tùy chọn), bấm vào dòng phiếu đề nghị cần chọn.')
    d.sub(['Hoặc bấm ', '@btn_dong_req', ' để không chọn.'])
    d.step('Bước 6: Hệ thống tự điền thông tin phiếu đề nghị và các dòng chi tiết, khóa ô Loại chi.')
    d.img('10b_filled', 'Màn hình Thêm phiếu sau khi chọn phiếu đề nghị')
    d.step('Bước 7: Nhập thông tin chung:')
    d.sub('Ngày hạch toán (bắt buộc): chọn ngày, không nhỏ hơn ngày hôm nay (mặc định là hôm nay).')
    d.sub('Tài khoản có, Tài khoản nợ (bắt buộc): đã điền sẵn theo phiếu đề nghị, chọn lại nếu cần.')
    d.sub('Tỷ giá (bắt buộc khi dùng ngoại tệ): số lớn hơn 0.')
    d.sub('Phương thức thanh toán (bắt buộc): chọn Tiền tự có hoặc Tiền vay.')
    d.sub('Ngân hàng chuyển (bắt buộc): chọn ngân hàng; đổi ngân hàng thì phải chọn lại Số tài khoản.')
    d.sub('Số tài khoản chuyển khoản (bắt buộc): chọn tài khoản của ngân hàng vừa chọn.')
    d.step('Bước 8: Ở bảng Chi tiết, nhập từng dòng:')
    d.sub('Số tiền duyệt chi (bắt buộc): lớn hơn 0 và không lớn hơn Số tiền đề nghị chi; dấu phẩy ngăn hàng nghìn, '
          'dấu chấm ngăn phần thập phân (ví dụ 1,200.5).')
    d.sub('Ghi chú (tùy chọn).')
    d.step(['Bước 9: Bấm ', '@btn_luuduyet', ', chọn ', '@btn_confirm_xacnhan',
            ' để chốt phiếu (ghi sổ kế toán, sau đó không sửa, không xóa được),'])
    d.img('14_approve', 'Hộp xác nhận lưu và duyệt')
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần Loại chi).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chi thu nhập cho nhân viên
    d.phan('LẬP PHIẾU CHI THU NHẬP CHO NHÂN VIÊN')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.step('Bước 3: Ở ô Loại chi, chọn “Chi thu nhập cho nhân viên”.')
    d.img('12_income', 'Màn hình Thêm phiếu loại Chi thu nhập cho nhân viên')
    d.step('Bước 4: Nhập thông tin chung:')
    d.sub('Người nhận (bắt buộc): tên người nhận tiền, tối đa 255 ký tự.')
    d.sub('Phòng ban (bắt buộc): chọn phòng ban chi; hệ thống lấy danh sách nhân viên còn số dư thu nhập.')
    d.sub('Lý do chi (bắt buộc): nhập chữ.')
    d.sub('Ngân hàng chuyển, Số tài khoản chuyển khoản (bắt buộc): chọn trong danh sách.')
    d.step('Bước 5: Ở tab Chi tiết, bỏ tích Cần thanh toán ở nhân viên không chi; nhập Số tiền chi (bắt buộc, không '
           'vượt Số dư) cho từng nhân viên còn tích.')
    d.step('Bước 6: Ở tab Chi tiết vụ việc, tách Số tiền chi thành 5 khoản; tổng 5 khoản phải bằng Số tiền chi.')
    d.img('12b_vuviec', 'Tab Chi tiết vụ việc')
    d.step(['Bước 7: Bấm ', '@btn_luuduyet', ', chọn ', '@btn_confirm_xacnhan', ' để chốt phiếu,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 4 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu ủy nhiệm chi”.')
    d.img('15_edit', 'Màn hình Sửa phiếu ủy nhiệm chi')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2, PHẦN 3; ô Loại chi không đổi được).')
    d.step(['Bước 5: Bấm ', '@btn_luuduyet', ', chọn ', '@btn_confirm_xacnhan', ' để chốt phiếu,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 5 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Mã phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 6 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Mã phiếu. Hệ thống mở màn “Chi tiết phiếu ủy nhiệm chi”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu ủy nhiệm chi')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 7 — Lịch sử (cột Hành động có sẵn biểu tượng Lịch sử, không có menu ba chấm)
    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step('Bước 1: Bấm vào Mã phiếu để mở màn chi tiết')
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

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
