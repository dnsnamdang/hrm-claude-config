# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu hạch toán mua dịch vụ (form chuẩn Danh mục quốc gia, 03/11/2026).

Chạy: python gen_hdsd.py  → HDSD_Yeu cau hach toan mua dich vu.docx (PDF + ảnh soát ghi vào thư mục tạm)
Phần chung: ../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py. Sơ đồ tổng quan dùng lại ảnh gen_srs.py sinh ra.
Khuôn cấu trúc: ../finance-addition-accounting-request/gen_hdsd.py.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu hạch toán mua dịch vụ'
SHOTS = os.path.join(HERE, 'ychtmdv_shots')
OUT = os.path.join(HERE, 'HDSD_Yeu cau hach toan mua dich vu.docx')
CHECK_DIR = os.path.join(tempfile.gettempdir(), 'hdsd_ychtmdv')

THUAT_NGU = [
    ['Phiếu yêu cầu hạch toán mua dịch vụ', 'Phiếu đề nghị kế toán hạch toán chi phí mua dịch vụ, số phiếu dạng TPE.YCHTMDV.2026000069.'],
    ['Loại yêu cầu', 'Dịch vụ thuê ngoài (lập từ hợp đồng mua dịch vụ) hoặc Công nợ bảo hiểm (lập từ đơn bảo hiểm).'],
    ['SL HĐ còn lại', 'Số lượng của hợp đồng chưa hạch toán và chưa bị phiếu khác giữ.'],
    ['SL hạch toán', 'Số lượng đề nghị hạch toán cho từng yêu cầu mua dịch vụ.'],
    ['Đang tạo', 'Phiếu lưu nháp; người tạo sửa / xóa được.'],
    ['Chờ duyệt', 'Phiếu đã gửi, chờ kế toán Hạch toán hoặc Không duyệt.'],
    ['Đang hạch toán / Đã hạch toán', 'Kế toán đã lưu nháp / đã duyệt phiếu Hạch toán mua dịch vụ lập từ phiếu này.'],
    ['Không duyệt', 'Kế toán trả về kèm Ghi chú duyệt; người tạo sửa lại rồi gửi duyệt lại.'],
]
PHIEN_BAN = [['1.0', '03/11/2026', 'Tạo mới tài liệu theo form chuẩn']]
QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel, xem lịch sử',
     'Phiếu do mình tạo luôn xem được. Xem rộng hơn cần một trong các quyền: Xem yêu cầu hạch toán mua dịch vụ - theo tổng công ty / '
     '- theo công ty / - theo phòng ban.'],
    ['Lập phiếu', 'Không cần quyền riêng; chỉ chọn được hợp đồng mua dịch vụ đã duyệt do mình tạo.'],
    ['Sửa, xóa', 'Người tạo phiếu; phiếu Đang tạo hoặc Không duyệt.'],
    ['Hạch toán, Không duyệt', 'Quyền Hạch toán mua dịch vụ, cùng công ty với phiếu; phiếu Chờ duyệt.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(SHOTS, 'uml', 'overview.png'))

    d.phan('TRUY CẬP VÀ TÌM KIẾM')
    d.p('Cách 1: Từ phân hệ Bán hàng:')
    d.step(['Bước 1: Từ phân hệ Bán hàng ', '@menu_phanhe_banhang', ', tại menu Yêu cầu ', '@menu_yeucau', ', nhóm Mua dịch vụ ',
            '@menu_nhom_muadv', ', chọn YC hạch toán mua dịch vụ ', '@menu_muc_sale'])
    d.p('Cách 2: Từ phân hệ Tài chính:')
    d.step(['Bước 1: Từ phân hệ Tài chính ', '@menu_phanhe_taichinh', ', tại menu Hàng hoá - Dịch vụ - Vận chuyển ', '@menu_hhdvvc',
            ', nhóm Mua dịch vụ ', '@menu_nhom_muadv_tc', ', chọn Yêu cầu hạch toán mua dịch vụ ', '@menu_muc_tc'])
    d.img('01_list', 'Màn hình Yêu cầu hạch toán mua dịch vụ')
    d.step(['Bước 2: Nhập số phiếu, số hợp đồng hoặc tên dịch vụ vào ô tìm kiếm nhanh ', '@o_timnhanh'])
    d.step(['Bước 3: Nhấn ', '@btn_timkiem'])
    d.step(['Bước 4: Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong ', '@o_trangthai', ' để lọc theo Trạng thái'])
    for lb, ic in [('Loại yêu cầu', 'o_loai'), ('Công ty', 'o_congty'), ('Phòng ban', 'o_phongban'), ('Nhà cung cấp', 'o_ncc'),
                   ('Người duyệt', 'o_nguoiduyet'), ('Người tạo', 'o_nguoitao'), ('Ngày tạo', 'o_ngaytao')]:
        d.sub(['Hoặc chọn giá trị ', '@' + ic, ' để lọc theo %s' % lb])
    d.step(['Bước 5: Chọn ', '@btn_lammoi', ' để xóa giá trị đã lọc'])

    d.phan('LẬP PHIẾU YÊU CẦU HẠCH TOÁN MUA DỊCH VỤ')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu hạch toán mua dịch vụ (PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10e_filled', 'Màn hình Tạo phiếu yêu cầu hạch toán mua dịch vụ')
    d.step(['Bước 3: Chọn Loại yêu cầu ', '@o_loai_form', ' (bắt buộc, mặc định Dịch vụ thuê ngoài).'])
    d.step(['Bước 4: Loại Dịch vụ thuê ngoài: bấm ô ', '@o_hopdong', ', tìm và bấm vào dòng hợp đồng cần lập (nút ',
            '@btn_timkiem_popup', ', ', '@btn_lammoi_popup', '). Hệ thống điền Nhà cung cấp và Danh sách dịch vụ.'])
    d.sub(['Hoặc bấm ', '@btn_dong_popup', ' để đóng cửa sổ chọn.'])
    d.sub('Loại Công nợ bảo hiểm: bấm ô Số đơn bảo hiểm, bấm vào dòng đơn cần lập; thông tin bảo hiểm tự điền.')
    d.step(['Bước 5: Kiểm tra Nhà cung cấp ', '@o_ncc_form', ', nhập SL hạch toán từng yêu cầu (không âm, không vượt SL HĐ còn lại).'])
    d.step(['Bước 6: Chọn Hóa đơn VAT ', '@o_vat', ' (bắt buộc khi gửi duyệt); nhập Diễn giải (không bắt buộc, tối đa 1.000 ký tự).'])
    d.step(['Bước 7: Bấm ', '@btn_themtailieu', ' để đính kèm file (bắt buộc khi chọn Kèm hóa đơn).'])
    d.step(['Bước 8: Bấm ', '@btn_luuguiduyet', ' để gửi kế toán'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần Loại yêu cầu).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' để không lưu, chọn ', '@btn_thoat', ' để rời màn hoặc ', '@btn_olai', ' để ở lại.'])

    d.phan('CHỈNH SỬA')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu hạch toán mua dịch vụ.')
    d.step(['Bước 2: Bấm ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo / Không duyệt do mình tạo.'])
    d.sub(['Hoặc bấm vào Số phiếu ', '@link_sophieu', ' để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu yêu cầu hạch toán mua dịch vụ”.')
    d.img('19_edit', 'Màn hình Sửa phiếu yêu cầu hạch toán mua dịch vụ')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc như PHẦN 2; Loại yêu cầu không đổi được). Phiếu Không duyệt: đọc Ghi chú duyệt '
           'rồi sửa lại.')
    d.step(['Bước 5: Bấm ', '@btn_luuguiduyet', ' để gửi duyệt'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai_form', ' nếu muốn hủy.'])

    d.phan('XÓA')
    d.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động của phiếu Đang tạo / Không duyệt do mình tạo; hệ thống mở màn chi tiết'])
    d.step(['Bước 2: Ở chân màn chi tiết, bấm ', '@btn_xoa', '. Hệ thống hiện hộp xác nhận “Xác nhận xóa”'])
    d.img('13_delete', 'Hộp xác nhận xóa phiếu')
    d.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
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
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu hạch toán mua dịch vụ.')
    d.step(['Bước 2: Bấm vào Số phiếu ', '@link_sophieu', '. Hệ thống mở màn “Chi tiết yêu cầu hạch toán mua dịch vụ”.'])
    d.img('17_detail', 'Màn hình Chi tiết yêu cầu hạch toán mua dịch vụ')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

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
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu hạch toán mua dịch vụ')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.p('Cách 2: In danh sách:')
    d.step('Bước 1: Lọc danh sách cần in (xem PHẦN 1).')
    d.step(['Bước 2: Bấm ', '@btn_indanhsach', ', rồi bấm ', '@btn_in_preview', ' trong cửa sổ xem trước.'])

    d.phan('HẠCH TOÁN (KẾ TOÁN)')
    d.step('Bước 1: Truy cập vào màn hình Yêu cầu hạch toán mua dịch vụ (PHẦN 1), lọc Trạng thái = Chờ duyệt.')
    d.step(['Bước 2: Bấm ', '@btn_hachtoan_row', ' ở cột Hành động'])
    d.sub(['Hoặc bấm Số phiếu để mở màn chi tiết, chọn ', '@btn_hachtoan'])
    d.step('Bước 3: Hệ thống mở màn “Tạo phiếu hạch toán mua dịch vụ” với phiếu yêu cầu điền sẵn.')
    d.img('21_accounting_create', 'Màn hình Tạo phiếu hạch toán mua dịch vụ')
    d.step('Bước 4: Hoàn thiện phiếu hạch toán theo HDSD màn Hạch toán mua dịch vụ, bấm Lưu và duyệt rồi chọn Duyệt để ghi sổ '
           '(hoặc Lưu nháp).')

    d.phan('KHÔNG DUYỆT (KẾ TOÁN)')
    d.step(['Bước 1: Ở cột Hành động của phiếu Chờ duyệt, bấm ', '@btn_khongduyet_row'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_khongduyet'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Không duyệt yêu cầu hạch toán mua dịch vụ”.')
    d.img('15_reject', 'Cửa sổ Không duyệt yêu cầu hạch toán mua dịch vụ')
    d.step('Bước 3: Nhập Ghi chú duyệt (bắt buộc, tối đa 255 ký tự).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_khongduyet', ' để xác nhận. Phiếu chuyển Không duyệt.'])
    d.sub(['Hoặc bấm ', '@btn_huy_reject', ' nếu muốn hủy.'])

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
