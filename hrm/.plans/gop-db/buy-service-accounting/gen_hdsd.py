# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Hạch toán mua dịch vụ (form chuẩn Danh mục quốc gia, 03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Hach toan mua dich vu.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra.
Khuôn cấu trúc: ../buy-service-accounting-request/gen_hdsd.py.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Hạch toán mua dịch vụ'
SHOTS = os.path.join(HERE, 'htmdv_shots')
OUT = os.path.join(HERE, 'HDSD_Hach toan mua dich vu.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_htmdv')

THUAT_NGU = [
    ['Phiếu hạch toán mua dịch vụ', 'Chứng từ kế toán ghi nhận chi phí mua dịch vụ, số phiếu dạng TPE.HTMDV.2026000060.'],
    ['Phiếu yêu cầu', 'Phiếu Yêu cầu hạch toán mua dịch vụ đang Chờ duyệt mà phiếu hạch toán được lập từ đó.'],
    ['Loại yêu cầu', 'Dịch vụ thuê ngoài hoặc Công nợ bảo hiểm — lấy theo phiếu yêu cầu.'],
    ['SL yêu cầu / SL hạch toán', 'Số lượng trên phiếu yêu cầu (mức tối đa) / số lượng kế toán ghi nhận.'],
    ['Đang tạo', 'Phiếu lưu nháp, chưa ghi sổ; người tạo sửa / xóa / duyệt được.'],
    ['Đã duyệt', 'Phiếu đã Lưu và duyệt: ghi bút toán vào sổ kế toán; không sửa, không xóa được.'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do mình tạo luôn xem được. Xem rộng hơn cần một trong các quyền: Xem hạch toán mua dịch vụ - theo tổng công ty / '
     '- theo công ty / - theo phòng ban.'],
    ['Lập phiếu, Lưu và duyệt', 'Quyền Hạch toán mua dịch vụ.'],
    ['Sửa, xóa', 'Quyền Hạch toán mua dịch vụ, là người tạo phiếu; phiếu Đang tạo.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.p('Cách 1: Từ phân hệ Bán hàng:')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe_banhang', ', tại menu Yêu cầu ', '@menu_yeucau', ', nhóm Mua dịch vụ ',
            '@menu_nhom_muadv', ', chọn Hạch toán mua dịch vụ ', '@menu_muc_sale'])
    d.p('Cách 2: Từ phân hệ Tài chính:')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe_taichinh', ', tại menu Hàng hoá - Dịch vụ - Vận chuyển ', '@menu_hhdvvc',
            ', nhóm Mua dịch vụ ', '@menu_nhom_muadv_tc', ', chọn Hạch toán mua dịch vụ ', '@menu_muc_tc'])
    d.img('01_list', 'Màn hình Hạch toán mua dịch vụ')
    d.step(['Bước 2: Nhập số phiếu, số phiếu yêu cầu hoặc số hợp đồng vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Loại yêu cầu', 'o_loai'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.sub(['Hoặc gõ vào ', '@o_ncc', ' / ', '@o_tendv', ' rồi nhấn Tìm kiếm để lọc theo Nhà cung cấp / Tên dịch vụ'])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('LẬP PHIẾU HẠCH TOÁN MUA DỊCH VỤ')
    d.p('Cách 1: Từ màn Hạch toán mua dịch vụ:')
    d.step('Bước 1: Truy cập vào màn hình Hạch toán mua dịch vụ (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi', ' (chỉ hiện với người có quyền Hạch toán mua dịch vụ)'])
    d.step(['Bước 3: Bấm ô Phiếu yêu cầu ', '@o_phieuyeucau', ', bấm vào dòng phiếu cần hạch toán (nút ', '@btn_timkiem_popup', ', ',
            '@btn_lammoi_popup', ')'])
    d.sub(['Hoặc bấm ', '@btn_dong_popup', ' để đóng cửa sổ chọn.'])
    d.img('11_request_picker', 'Cửa sổ Chọn phiếu yêu cầu hạch toán mua dịch vụ')
    d.p('Cách 2: Từ màn Yêu cầu hạch toán mua dịch vụ:')
    d.step(['Bước 1: Ở dòng phiếu yêu cầu Chờ duyệt, bấm ', '@btn_hachtoan_yc', '. Hệ thống mở màn Tạo phiếu với phiếu yêu cầu chọn sẵn.'])
    d.p('Hoàn thiện phiếu:')
    d.img('10e_filled', 'Màn hình Tạo phiếu hạch toán mua dịch vụ')
    d.step('Bước 4: Hệ thống tự điền Loại yêu cầu, Hợp đồng, Nhà cung cấp, Hóa đơn VAT, bảng dịch vụ (SL hạch toán = SL yêu cầu) và file '
           'của phiếu yêu cầu; Tài khoản có mặc định 3311.')
    d.step(['Bước 5: Chọn Tài khoản nợ ', '@o_tkno', ' (bắt buộc khi duyệt); kiểm tra Tài khoản có ', '@o_tkco', ' và Nhà cung cấp ',
            '@o_ncc_form'])
    d.step(['Bước 6: Kiểm tra Hóa đơn VAT ', '@o_vat', '; nhập Diễn giải ', '@o_diengiai', ' (không bắt buộc, tối đa 1.000 ký tự).'])
    d.step('Bước 7: Ở bảng Chi tiết, sửa Đơn giá, SL hạch toán (không âm, không vượt SL yêu cầu); chọn Mã phí / Mã vụ việc ở dòng đầu '
           'để áp cho mọi dòng (bắt buộc khi Tài khoản nợ thuộc nhánh 642 / 154).')
    d.step(['Bước 8: Bấm ', '@btn_themtailieu', ' để đính kèm file (bắt buộc khi Kèm hóa đơn).'])
    d.step(['Bước 9: Bấm ', '@btn_luunhap', ' để lưu nháp (chỉ cần Phiếu yêu cầu)'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để ghi sổ (xem PHẦN 3).'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('LƯU VÀ DUYỆT (GHI SỔ)')
    d.step('Bước 1: Ở màn Tạo hoặc màn Sửa phiếu Đang tạo, nhập đủ thông tin (PHẦN 2).')
    d.step(['Bước 2: Bấm ', '@btn_luuduyet', '. Thiếu thông tin thì hệ thống báo đỏ dưới ô; đủ thì hiện hộp “Xác nhận duyệt”.'])
    d.img('14_approve_confirm', 'Hộp Xác nhận duyệt')
    d.step(['Bước 3: Bấm ', '@btn_duyet_confirm', ' để ghi sổ. Phiếu chuyển Đã duyệt, phiếu yêu cầu chuyển Đã hạch toán.'])
    d.sub(['Hoặc bấm ', '@btn_huy_duyet', ' để quay lại form.'])

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Hạch toán mua dịch vụ.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình tạo.'])
    d.sub(['Hoặc bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu hạch toán mua dịch vụ”.')
    d.img('19_edit', 'Màn hình Sửa phiếu hạch toán mua dịch vụ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc như PHẦN 2; Phiếu yêu cầu không đổi được).')
    d.step(['Bước 5: Bấm ', '@btn_luunhap', ' để lưu'])
    d.sub(['Hoặc ', '@btn_luuduyet', ' để ghi sổ.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' nếu muốn hủy.'])

    d.phan('XÓA')
    d.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đang tạo do mình tạo'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_xoa'])
    d.step('Bước 2: Hệ thống hiện hộp xác nhận “Xác nhận xóa”.')
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa. Phiếu yêu cầu trở lại Chờ duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    d.phan('XEM LỊCH SỬ THAY ĐỔI')
    d.p('Cách 1: Xem lịch sử từ màn danh sách:')
    d.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
    d.p('Cách 2: Xem lịch sử từ màn chi tiết:')
    d.step(['Bước 1: Bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết'])
    d.step(['Bước 2: Ở khối Lịch sử, chọn nút ', '@btn_xemlichsu'])
    d.img('16_history', 'Cửa sổ Lịch sử thay đổi của phiếu')
    d.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
    d.step(['Bước 4: Bấm ', '@btn_dong_ls', ' để đóng cửa sổ.'])

    d.phan('XEM CHI TIẾT')
    d.step('Bước 1: Truy cập vào màn hình Hạch toán mua dịch vụ.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết hạch toán mua dịch vụ”.'])
    d.sub(['Bấm Phiếu yêu cầu ', '@link_phieuyeucau', ' để mở phiếu yêu cầu ở tab mới.'])
    d.img('17_detail', 'Màn hình Chi tiết hạch toán mua dịch vụ')
    d.step('Bước 3: Kéo xuống khối Hạch toán để xem các bút toán Nợ / Có của phiếu Đã duyệt.')
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    d.phan('XUẤT EXCEL')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “Chọn trường xuất file”.'])
    d.img('20_export', 'Cửa sổ Chọn trường xuất file')
    d.step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
    d.sub(['Hoặc bấm ', '@btn_chontatca', ' / ', '@btn_bochonhet'])
    d.step(['Bước 4: Bấm ', '@btn_xuatfile'])
    d.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
    d.step('Bước 5: Mở file Excel đã tải.')

    d.tuy_chinh_cot()

    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.p('Cách 1: In một phiếu:')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu hạch toán mua dịch vụ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.p('Cách 2: In danh sách:')
    d.step('Bước 1: Lọc danh sách cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_indanhsach', ', rồi bấm ', '@btn_in_preview', ' trong cửa sổ xem trước.'])

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
